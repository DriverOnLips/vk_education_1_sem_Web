from django.shortcuts import render
from . import models
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models import Count
import random


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    question_list = models.Question.objects.prefetch_related(
        Prefetch('answer_to_question'),
    ).annotate(num_answers=Count('answer_to_question')).all()
    questions = paginate(question_list, request, 10)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'questions': questions,
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    if not models.Question.objects.with_id(question_id).exists():
        question = models.Question.objects.random()
        question_id = question.get_id()
    else:
        question = models.Question.objects.get(id=question_id)
    answer_list = models.Answer.objects.filter(to_question=question_id)
    answers = paginate(answer_list, request, 10)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {'question': question,
               'answers': answers,
               'best_members': best_members,
               'popular_tags': popular_tags,
               'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
               }
    return render(request, 'question.html', context)


def ask(request):
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_templates': ['inc/navbar_registered.html'],
    }
    return render(request, 'ask.html', context)


def login(request):
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_templates': ['inc/navbar_viewed.html'],
    }
    return render(request, 'login.html', context)


def tag(request, tag_name):
    question_list = models.Question.objects.with_tag(tag_name).select_related('author') \
        .prefetch_related(Prefetch('answer_to_question')).annotate(num_answers=
        Count('answer_to_question')).all()
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
        'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
    }
    return render(request, 'tag.html', context)



def signup(request):
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_templates': ['inc/navbar_viewed.html'],
    }
    return render(request, 'signup.html', context)


def user(request):
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {
        'best_members': best_members,
        'popular_tags': popular_tags,
        'navbar_templates': ['inc/navbar_registered.html'],
    }
    return render(request, 'user.html', context)


def hot(request):
    question_list = models.Question.objects.prefetch_related(
        Prefetch('tag', queryset=models.Tag.objects.all()),
        Prefetch('answer_to_question'),
    ).annotate(num_answers=Count('answer_to_question')).all()
    hot_questions = random.sample(list(question_list), k=25)
    best_members = random.sample(list(models.User.objects.all()), k=5)
    popular_tags = random.sample(list(models.Tag.objects.all()), k=12)
    context = {'questions': hot_questions,
               'best_members': best_members,
               'popular_tags': popular_tags,
               'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
               }
    return render(request, 'hot.html', context)


def base(request):
    return render(request, 'inc/base.html')


