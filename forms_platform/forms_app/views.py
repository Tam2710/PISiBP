from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from copy import deepcopy
import openpyxl

from .models import User, Formular, Question, Option, FilledForm, Answer, Collaborator
from .serializers import (
    UserSerializer,
    FormularSerializer,
    QuestionSerializer,
    FilledFormSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# ------------------ USER REGISTER / LOGIN ------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type,
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------ USERS ------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# ------------------ FORMULAR ------------------
class FormularViewSet(viewsets.ModelViewSet):
    queryset = Formular.objects.all()
    serializer_class = FormularSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # Kloniranje forme
    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        form = self.get_object()
        cloned_form = deepcopy(form)
        cloned_form.id = None
        cloned_form.name += " (Copy)"
        cloned_form.creator = request.user
        cloned_form.save()

        for question in form.questions.all():
            cloned_question = deepcopy(question)
            cloned_question.id = None
            cloned_question.form = cloned_form
            cloned_question.save()

            for option in question.options.all():
                cloned_option = deepcopy(option)
                cloned_option.id = None
                cloned_option.question = cloned_question
                cloned_option.save()

        serializer = self.get_serializer(cloned_form)
        return Response(serializer.data)

    # Pregled rezultata popunjenih formi
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        form = self.get_object()
        if not (form.creator == request.user or form.collaborators.filter(pk=request.user.id).exists()):
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        filled_forms = FilledForm.objects.filter(form=form)
        data = []
        for ff in filled_forms:
            answers = [
                {
                    "question": a.question.text,
                    "value": a.value,
                    "options": [o.text for o in a.selected_options.all()],
                }
                for a in ff.answers.all()
            ]
            data.append({
                "filled_form_id": ff.id,
                "user": ff.user.username if ff.user else "Anonymous",
                "answers": answers,
            })

        return Response(data)

    # Izvoz rezultata u Excel
    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        form = self.get_object()
        if not (form.creator == request.user or form.collaborators.filter(pk=request.user.id).exists()):
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = form.name

        headers = ["User"]
        for q in form.questions.all():
            headers.append(q.text)
        ws.append(headers)

        for ff in FilledForm.objects.filter(form=form):
            row = [ff.user.username if ff.user else "Anonymous"]
            for q in form.questions.all():
                answer = ff.answers.filter(question=q).first()
                if answer:
                    if q.type in ['single_choice', 'multi_choice']:
                        row.append(", ".join([o.text for o in answer.selected_options.all()]))
                    else:
                        row.append(answer.value or "")
                else:
                    row.append("")
            ws.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{form.name}.xlsx"'
        wb.save(response)
        return response


# ------------------ FILLED FORM ------------------
class FilledFormViewSet(viewsets.ModelViewSet):
    queryset = FilledForm.objects.all()
    serializer_class = FilledFormSerializer
    permission_classes = [permissions.AllowAny]


# ------------------ COLLABORATORS ------------------
class CollaboratorViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add(self, request, pk=None):
        form = get_object_or_404(Formular, pk=pk)
        if form.creator != request.user:
            return Response({"error": "Only owner can manage collaborators"}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        role = request.data.get('role', 'observer')
        user = get_object_or_404(User, pk=user_id)
        Collaborator.objects.update_or_create(user=user, form=form, defaults={'role': role})
        return Response({"status": "collaborator added"})

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        form = get_object_or_404(Formular, pk=pk)
        if form.creator != request.user:
            return Response({"error": "Only owner can manage collaborators"}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        Collaborator.objects.filter(user_id=user_id, form=form).delete()
        return Response({"status": "collaborator removed"})
