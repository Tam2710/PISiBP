from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User, Formular, Question, Option, FilledForm, Answer
from .serializers import UserSerializer, FormularSerializer, QuestionSerializer, FilledFormSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class FormularViewSet(viewsets.ModelViewSet):
    queryset = Formular.objects.all()
    serializer_class = FormularSerializer
    permission_classes = [permissions.IsAuthenticated]

class FilledFormViewSet(viewsets.ModelViewSet):
    queryset = FilledForm.objects.all()
    serializer_class = FilledFormSerializer
    permission_classes = [permissions.AllowAny]  # Ako forma dozvoljava anonimno
