from rest_framework import serializers
from .models import User, Formular, Question, Option, FilledForm, Answer, Collaborator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'image']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'required', 'image', 'options']

class FormularSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    
    class Meta:
        model = Formular
        fields = ['id', 'name', 'description', 'allow_anonymous', 'is_locked', 'questions']

class AnswerSerializer(serializers.ModelSerializer):
    selected_options = OptionSerializer(many=True, required=False)
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'value', 'selected_options']

class FilledFormSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = FilledForm
        fields = ['id', 'form', 'user', 'created_at', 'answers']
