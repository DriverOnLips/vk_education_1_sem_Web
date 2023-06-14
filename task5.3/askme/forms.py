import os
import io
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

from askme_py_files import settings
from . import models


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Please enter a correct %(username)s and password.',
    }
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    photo = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['name', 'email', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password and password_check and password != password_check:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)
        if commit:
            user.save()

        photo_file = self.cleaned_data.get('photo')
        if photo_file:
            photo_name = photo_file.name
            photo_path = os.path.join(settings.MEDIA_ROOT, photo_name)
            with open(photo_path, 'wb') as f:
                for chunk in photo_file.chunks():
                    f.write(chunk)
            user.photo = photo_name
            user.save()

        return user


class QuestionForm(forms.ModelForm):
    tag = forms.CharField(max_length=255)

    class Meta:
        model = models.Question
        fields = ['title', 'text',]

    def save(self, commit=True, author=None):
        question = super().save(commit=False)
        question.author = author
        if commit:
            question.save()

        tags = self.cleaned_data.get('tag')
        tags = [tag.strip() for tag in tags.split(',')]

        questionTags = []
        for tag in tags:
            print(tag)
            if not models.Tag.objects.with_name(name=tag).exists():
                questionTag = models.Tag(name=tag)
                questionTag.save()
            else:
                questionTag = models.Tag.objects.get(name=tag)
            questionTags.append(questionTag)

        question.tag.set(questionTags)

        return question


class AnswerForm(forms.ModelForm):
    to_question_id = forms.IntegerField(widget=forms.HiddenInput())
    answer = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = models.Answer
        fields = ('answer',)

    def save(self, commit=True, author=None):
        answer = super().save(commit=False)
        answer.author = author
        question_id = self.cleaned_data['to_question_id']
        answer.to_question = models.Question.objects.get(id=question_id)
        answer.status = 'u'
        answer.rating = 0
        answer.text = self.cleaned_data['answer']
        if commit:
            answer.save()
        return answer


class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['email', 'name', 'photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if email:
            user.email = email
        if password:
            user.password = make_password(password)

        if commit:
            user.save()

        photo_file = self.cleaned_data.get('photo')
        if photo_file == user.photo.name:
            pass
        elif photo_file:
            photo_name = photo_file.name
            photo_path = os.path.join(settings.MEDIA_ROOT, photo_name)
            with open(photo_path, 'wb') as f:
                for chunk in photo_file.chunks():
                    f.write(chunk)
            user.photo = photo_name
            user.save()
        else:
            photos_dir = 'media/photos'
            photo_filename = 'default.jpg'
            with open(os.path.join(photos_dir, photo_filename), "rb") as photo_file:
                photo_content = photo_file.read()
                photo = ContentFile(photo_content, photo_filename)
                user.photo = photo
                user.save()

        return user
