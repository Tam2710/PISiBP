from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

class Formular(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_forms')
    collaborators = models.ManyToManyField(User, blank=True, related_name='collaborations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Collaborator(models.Model):
    ROLE_CHOICES = (('editor', 'Editor'), ('observer', 'Observer'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Formular, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Question(models.Model):
    QUESTION_TYPES = (
        ('short_text', 'Short Text'),
        ('long_text', 'Long Text'),
        ('single_choice', 'Single Choice'),
        ('multi_choice', 'Multi Choice'),
        ('numeric', 'Numeric'),
        ('date', 'Date'),
        ('time', 'Time'),
    )
    form = models.ForeignKey(Formular, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    required = models.BooleanField(default=True)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='options/', blank=True, null=True)

class FilledForm(models.Model):
    form = models.ForeignKey(Formular, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    filled_form = models.ForeignKey(FilledForm, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)
    selected_options = models.ManyToManyField(Option, blank=True)
