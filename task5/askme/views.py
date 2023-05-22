from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
import random

from django.views.decorators.http import require_http_methods, require_POST

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
@require_http_methods(['GET', 'POST'])
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


@login_required()
@require_POST
def vote_question(request):
    question = models.Question.objects.get(id=request.POST['question_id'])
    mark_name = request.POST.get('mark_name', 'like')
    user = request.user

    if mark_name == 'like':
        if models.Mark2Question.objects.withParams(question, user, 'l').exists():
            models.Mark2Question.objects.withParams(question, user, 'l').delete()
            question.rating -= 1
        elif models.Mark2Question.objects.withParams(question, user, 'd').exists():
            models.Mark2Question.objects.withParams(question, user, 'd').delete()
            mark = models.Mark2Question(to_question=question, from_user=user, name='l')
            mark.save()
            question.rating += 2
        else:
            mark = models.Mark2Question(to_question=question, from_user=user, name='l')
            mark.save()
            question.rating += 1
    elif mark_name == 'dislike':
        if models.Mark2Question.objects.withParams(question, user, 'd').exists():
            models.Mark2Question.objects.withParams(question, user, 'd').delete()
            question.rating += 1
        elif models.Mark2Question.objects.withParams(question, user, 'l').exists():
            models.Mark2Question.objects.withParams(question, user, 'l').delete()
            mark = models.Mark2Question(to_question=question, from_user=user, name='d')
            mark.save()
            question.rating -= 2
        else:
            mark = models.Mark2Question(to_question=question, from_user=user, name='d')
            mark.save()
            question.rating -= 1
    question.save()

    return JsonResponse({'new_rating': question.rating})


@login_required()
@require_POST
def vote_answer(request):
    answer = models.Answer.objects.get(id=request.POST['answer_id'])
    mark_name = request.POST.get('mark_name', 'like')
    user = request.user

    if mark_name == 'like':
        if models.Mark2Answer.objects.withParams(answer, user, 'l').exists():
            models.Mark2Answer.objects.withParams(answer, user, 'l').delete()
            answer.rating -= 1
        elif models.Mark2Answer.objects.withParams(answer, user, 'd').exists():
            models.Mark2Answer.objects.withParams(answer, user, 'd').delete()
            mark = models.Mark2Answer(to_answer=answer, from_user=user, name='l')
            mark.save()
            answer.rating += 2
        else:
            mark = models.Mark2Answer(to_answer=answer, from_user=user, name='l')
            mark.save()
            answer.rating += 1
    elif mark_name == 'dislike':
        if models.Mark2Answer.objects.withParams(answer, user, 'd').exists():
            models.Mark2Answer.objects.withParams(answer, user, 'd').delete()
            answer.rating += 1
        elif models.Mark2Answer.objects.withParams(answer, user, 'l').exists():
            models.Mark2Answer.objects.withParams(answer, user, 'l').delete()
            mark = models.Mark2Answer(to_answer=answer, from_user=user, name='d')
            mark.save()
            answer.rating -= 2
        else:
            mark = models.Mark2Answer(to_answer=answer, from_user=user, name='d')
            mark.save()
            answer.rating -= 1
    answer.save()

    return JsonResponse({'new_rating': answer.rating})


@login_required()
@require_POST
def vote_correct(request):
    answer_id = request.POST.get('answer_id')
    answer = models.Answer.objects.get(id=answer_id)
    is_correct = request.POST.get('is_correct')
    user = request.user

    if is_correct:
        answer.status = 'c'
    else:
        answer.status = 'u'

    answer.save()

    return JsonResponse({'is_correct': answer.status})
