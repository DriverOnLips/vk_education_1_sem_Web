from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
import random
from . import models
from . import forms
from django.urls import reverse


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    if request.user.is_authenticated:
        navbarTemplate = 'inc/navbar_registered.html'
    else:
        navbarTemplate = 'inc/navbar_viewed.html'
    question_list = models.Question.objects.latestWithAnswers()
    questions = paginate(question_list, request, 10)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'questions': questions,
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': navbarTemplate,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def question(request, question_id):
    if request.user.is_authenticated:
        navbarTemplate = 'inc/navbar_registered.html'
    else:
        navbarTemplate = 'inc/navbar_viewed.html'

    if not models.Question.objects.with_id(question_id).exists():
        question = models.Question.objects.random()
        question_id = question.get_id()
    else:
        question = models.Question.objects.get(id=question_id)

    answer_list = models.Answer.objects.toQuestionId(question_id)
    answers = paginate(answer_list, request, 10)

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('question', question_id=question_id)
    else:
        form = forms.AnswerForm()

    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {'question': question,
               'answers': answers,
               'best_members': best_members,
               'popular_tags': popular_tags,
               'navbar_template': navbarTemplate,
               'form': form,
               }

    return render(request, 'question.html', context)


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def ask(request):
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(author=request.user)
            return redirect('question', question_id=question.id)
    else:
        form = forms.QuestionForm()

    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': 'inc/navbar_registered.html',
        'form': form,
    }
    return render(request, 'ask.html', context)



def tag(request, tag_name):
    if request.user.is_authenticated:
        navbarTemplate = 'inc/navbar_registered.html'
    else:
        navbarTemplate = 'inc/navbar_viewed.html'
    question_list = models.Question.objects.withTagAndAnswers(tag_name)
    if not question_list:
        pass
    questions = paginate(question_list, request, 10)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'questions': questions,
        'tag_name': tag_name,
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': navbarTemplate,
    }
    return render(request, 'tag.html', context)


@csrf_protect
def login(request):
    if request.method == 'GET':
        login_form = AuthenticationForm()
    elif request.method == 'POST':
        login_form = forms.LoginForm(data=request.POST)

        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                continue_url = request.GET.get('continue')
                if continue_url:
                    return redirect(continue_url)
                else:
                    return redirect('index')

    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': 'inc/navbar_viewed.html',
        'form': login_form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def signup(request):
    if request.method == 'GET':
        user_form = forms.RegistrationForm()
    elif request.method == 'POST':
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                auth.login(request, user)
                return redirect('index')
            else:
                user_form.add_error(field=None, error='User saving error!')

    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': 'inc/navbar_viewed.html',
        'form': user_form,
    }
    return render(request, 'signup.html', context)


@login_required(login_url='/login/', redirect_field_name='continue')
def user(request):
    if request.method == 'POST':
        form = forms.EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = forms.EditUserForm(instance=request.user)

    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_template': 'inc/navbar_registered.html',
        'user': request.user,
        'form': form,
    }
    return render(request, 'user.html', context)



def hot(request):
    if request.user.is_authenticated:
        navbarTemplate = 'inc/navbar_registered.html'
    else:
        navbarTemplate = 'inc/navbar_viewed.html'
    question_list = models.Question.objects.hot()
    hot_questions = random.sample(list(question_list), k=25)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {'questions': hot_questions,
               'best_members': best_members,
               'popular_tags': popular_tags,
               'navbar_template': navbarTemplate,
               }
    return render(request, 'hot.html', context)


def base(request):
    return render(request, 'inc/base.html')


