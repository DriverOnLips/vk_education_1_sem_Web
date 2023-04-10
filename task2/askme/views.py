from django.shortcuts import render, redirect
from . import models
from django.core.paginator import Paginator


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    question_list = models.QUESTIONS
    questions = paginate(question_list, request, 5)
    context = {
        'questions': questions,
        'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    if question_id > len(models.QUESTIONS):
        question_id = len(models.QUESTIONS)
    question = models.QUESTIONS[int(question_id) - 1]
    answer_list = [a for a in models.ANSWERS if a['title'] == question['title']]
    answers = paginate(answer_list, request, 3)
    context = {'question': question,
               'answers': answers,
               'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
               }
    return render(request, 'question.html', context)


def ask(request):
    context = {
        'navbar_templates': ['inc/navbar_registered.html'],
    }
    return render(request, 'ask.html', context)


def login(request):
    context = {
        'navbar_templates': ['inc/navbar_viewed.html'],
    }
    return render(request, 'login.html', context)


def tag(request, tag_name):
    question_list = [q for q in models.QUESTIONS if tag_name in q['tags']]
    if not question_list:
        question_list = [q for q in models.QUESTIONS if 'machine learning' in q['tags']]
    questions = paginate(question_list, request, 5)
    context = {
        'questions': questions,
        'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
        'tag_name': tag_name
    }
    return render(request, 'tag.html', context)



def signup(request):
    context = {
        'navbar_templates': ['inc/navbar_viewed.html'],
    }
    return render(request, 'signup.html', context)


def user(request):
    context = {
        'navbar_templates': ['inc/navbar_registered.html'],
    }
    return render(request, 'user.html', context)


def hot(request):
    question_list = models.QUESTIONS
    questions = paginate(question_list, request, 5)
    context = {'questions': questions,
               'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
               }
    return render(request, 'hot.html', context)


def base(request):
    context = {
        'navbar_templates': ['inc/navbar_registered.html', 'inc/navbar_viewed.html'],
    }
    return render(request, 'inc/base.html', context)


