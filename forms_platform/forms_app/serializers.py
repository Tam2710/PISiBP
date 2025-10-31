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
        # Kreiranje korisnika sa hashovanom lozinkom
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

    class Meta:
        model = Option
        fields = ['id', 'text', 'image']


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
    collaborators = UserEmailSerializer(read_only=True, many=True)
    questions = QuestionSerializer(many=True, required=False)

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

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        form = Formular.objects.create(**validated_data)

        for question_data in questions_data:
            options_data = question_data.pop('options', [])
            question = Question.objects.create(form=form, **question_data)
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)

        return form


# ---------------------- ANSWER SERIALIZER ----------------------
class AnswerSerializer(serializers.ModelSerializer):
    selected_options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'value', 'selected_options']


# ---------------------- FILLED FORM SERIALIZER ----------------------
class FilledFormSerializer(serializers.ModelSerializer):
    user = UserEmailSerializer(read_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = FilledForm
        fields = ['id', 'form', 'user', 'created_at', 'answers']


# ---------------------- COLLABORATOR SERIALIZER ----------------------
class CollaboratorSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(read_only=True)
    collaborator = UserEmailSerializer(read_only=True)

    class Meta:
        model = Collaborator
        fields = ['id', 'form', 'collaborator']
