from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Formular, Question, Option, FilledForm, Answer, Collaborator


User = get_user_model()


# ---------------------- USER SERIALIZER ----------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user


class UserEmailSerializer(serializers.ModelSerializer):
    """Kratka verzija korisnika — koristi se u formama"""
    class Meta:
        model = User
        fields = ['id', 'email']


# ---------------------- OPTION SERIALIZER ----------------------
class OptionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = Option
        fields = ['id', 'question', 'text', 'image']

# ---------------------- QUESTION SERIALIZER ----------------------
class QuestionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'required', 'image', 'options']


# ---------------------- FORM SERIALIZER ----------------------
class FormularSerializer(serializers.ModelSerializer):
    creator = UserEmailSerializer(read_only=True)
    collaborators = UserEmailSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Formular
        fields = [
            'id',
            'name',
            'description',
            'allow_anonymous',
            'is_locked',
            'creator',
            'collaborators',
            'created_at',
            'questions'
        ]

    def get_questions(self, obj):
        """Bezbedno serijalizuje pitanja i opcije"""
        questions = obj.questions.all()
        return QuestionSerializer(questions, many=True).data

    def create(self, validated_data):
        """Ručno kreira formu i pitanja iz FormData."""
        request = self.context['request']

        form = Formular.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description', ''),
            allow_anonymous=request.data.get('allow_anonymous') in ['true', True, 'on'],
            creator=request.user
        )

        i = 0
        while True:
            text = request.data.get(f'questions[{i}][text]')
            if not text:
                break
            q_type = request.data.get(f'questions[{i}][type]', 'short_text')
            required = request.data.get(f'questions[{i}][required]', 'true') in ['true', True, 'on']
            image = request.FILES.get(f'questions[{i}][image]')

            question = Question.objects.create(
                form=form, text=text, type=q_type, required=required, image=image
            )

            j = 0
            while True:
                opt_text = request.data.get(f'questions[{i}][options][{j}][text]')
                if not opt_text:
                    break
                opt_image = request.FILES.get(f'questions[{i}][options][{j}][image]')
                Option.objects.create(question=question, text=opt_text, image=opt_image)
                j += 1

            i += 1

        #  sada vraćamo Django instancu, ne dict
        return form



# ---------------------- ANSWER SERIALIZER ----------------------
class AnswerSerializer(serializers.ModelSerializer):
    selected_options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'value', 'selected_options']


# ---------------------- FILLED FORM SERIALIZER ----------------------
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'value', 'selected_options']

class FilledFormSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)

    class Meta:
        model = FilledForm
        fields = ['id', 'form', 'user', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        request = self.context.get('request')

        # Ako je korisnik prijavljen
        user = request.user if request and request.user.is_authenticated else None

        filled_form = FilledForm.objects.create(user=user, **validated_data)

        for answer_data in answers_data:
            options = answer_data.pop('selected_options', [])
            answer = Answer.objects.create(filled_form=filled_form, **answer_data)
            if options:
                answer.selected_options.set(options)

        return filled_form

# ---------------------- COLLABORATOR SERIALIZER ----------------------
class CollaboratorSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(read_only=True)
    collaborator = UserEmailSerializer(read_only=True)

    class Meta:
        model = Collaborator
        fields = ['id', 'form', 'collaborator']
