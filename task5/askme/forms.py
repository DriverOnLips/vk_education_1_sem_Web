from django import forms
from django.contrib.auth.forms import AuthenticationForm
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

    class Meta:
        model = models.User
        fields = ['name', 'email', 'photo']

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        user = models.User.objects.create_user(**self.cleaned_data)
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
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = models.Answer
        fields = ('text',)

    def save(self, commit=True, author=None):
        answer = super().save(commit=False)
        answer.author = author
        question_id = self.cleaned_data['to_question_id']
        answer.to_question = models.Question.objects.get(id=question_id)
        answer.status = 'u'
        answer.rating = 0
        if commit:
            answer.save()
        return answer


class EditUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'name', 'photo']
