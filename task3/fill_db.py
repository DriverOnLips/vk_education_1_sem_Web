import os
import sys
import django
import random
import nltk
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme_py_files.settings')
django.setup()

from django.db import connections, DEFAULT_DB_ALIAS
from askme.models import Question, User, Tag, Mark, Answer


nltk.download('gutenberg')
corpus = nltk.corpus.gutenberg.words()
words_dict = [word.lower() for word in corpus if len(word) >= 4]

def reset_sequence(table_name):
    with connections[DEFAULT_DB_ALIAS].cursor() as cursor:
        cursor.execute(f'UPDATE sqlite_sequence SET seq = 0 WHERE name = "{table_name}";')


def generate_users(num):
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Isabel', 'John',
             'Karen', 'Lucy', 'Michael', 'Nancy', 'Oliver', 'Pamela', 'Quinn', 'Ralph', 'Samantha',
             'Thomas', 'Uma', 'Victor', 'William', 'Xander', 'Yara', 'Zara']
    surnames = ['Smith', 'Johnson', 'Brown', 'Garcia', 'Miller', 'Taylor', 'Wilson', 'Jackson',
                'Clark', 'Campbell', 'Young', 'Lee', 'Perez', 'Hall', 'Allen', 'Adams', 'King',
                'Wright', 'Scott', 'Baker', 'Gonzalez', 'Carter', 'Mitchell', 'Turner', 'Parker']
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'mail.com', 'mail.ru', 'vk.com',
               'yandex.com', 'yandex.ru']
    users = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    photos_dir = "static/img/photos"
    for i in range(num):
        name = random.choice(names) + ' ' + random.choice(surnames)
        email = f'{name.lower().replace(" ", ".")}{str(random.randint(1, 9999))}' \
                f'@{random.choice(domains)}'
        if not User.objects.with_email(email).exists():
            rating = random.randint(0, 100)

            photo_filenames = [f for f in os.listdir(photos_dir) if
                               os.path.isfile(os.path.join(photos_dir, f)) and f.lower().endswith(
                                   tuple(image_extensions))]
            photo_filename = random.choice(photo_filenames)
            with open(os.path.join(photos_dir, photo_filename), "rb") as photo_file:
                photo_content = photo_file.read()
                photo = ContentFile(photo_content, photo_filename)
                user = User(email=email, rating=rating, name=name,
                            photo=photo)
                user.set_password("password")
                users.append(user)
    User.objects.bulk_create(users)


def generate_tags(num):
    tags = []
    for i in range(num):
        name = random.choice(words_dict)
        if not Tag.objects.with_name(name=name).exists():
            tag = Tag(name=name)
            tags.append(tag)
    Tag.objects.bulk_create(tags)


def generate_marks(num):
    STATUS_CHOICES = [
        ('l', 'like'),
        ('d', 'dislike'),
    ]
    marks = []
    for i in range(num):
        name = random.choice(STATUS_CHOICES)
        to_user = User.objects.random()
        from_user = User.objects.random()
        while from_user == to_user:
            from_user = User.objects.random()
        mark = Mark(to_user=to_user, from_user=from_user, name=name[0])
        marks.append(mark)
    Mark.objects.bulk_create(marks)


def generate_questions(num):
    questions = []
    for i in range(num):
        title = f'Question {str(random.randint(1, 2000000))}'
        if not Question.objects.with_title(title).exists():
            text = ' '.join(random.choices(words_dict, k=40))
            author = User.objects.random()
            question = Question(title=title, text=text, author=author)
            question.save()
            question.tag.set([Tag.objects.random() for _ in range(4)])
            questions.append(question)


def generate_answers(num):
    STATUS_CHOICES = [
        ('r', 'right'),
        ('u', 'unknown')
    ]
    answers = []
    for i in range(num):
        to_question = Question.objects.random()
        author = User.objects.random()
        text = ' '.join(random.choices(words_dict, k=70))
        status = random.choice(STATUS_CHOICES)
        answer = Answer(to_question=to_question, author=author, text=text, status=status[0])
        answers.append(answer)
    Answer.objects.bulk_create(answers)


def fill_db(num):
    generate_users(num)
    generate_marks(200*num)
    generate_tags(num)
    generate_questions(10 * num)
    generate_answers(100 * num)


if __name__ == '__main__':
    User.objects.all().delete()
    Tag.objects.all().delete()
    Mark.objects.all().delete()
    Question.objects.all().delete()
    Answer.objects.all().delete()

    reset_sequence('Tags')
    reset_sequence('Users')
    reset_sequence('Marks')
    reset_sequence('Questions')
    reset_sequence('Answers')
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    fill_db(num)