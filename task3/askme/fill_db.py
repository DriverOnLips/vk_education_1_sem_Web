import os
import sys
import django
import random
import nltk
from django.core.files import File
from django.db import connections, DEFAULT_DB_ALIAS
from models import Question, User, Tag, Mark, Answer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task3.askme_py_files.settings')
django.setup()

nltk.download('gutenberg')
corpus = nltk.corpus.gutenberg.words()


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
        rating = random.randint(0, 100)

        if not User.objects.with_email(email).exists():
            photo_filenames = [f for f in os.listdir(photos_dir) if
                               os.path.isfile(os.path.join(photos_dir, f)) and f.lower().endswith(
                                   tuple(image_extensions))]
            photo_filename = random.choice(photo_filenames)
            with open(os.path.join(photos_dir, photo_filename), 'rb') as photo_file:
                user = User(email=email, rating=rating, name=name,
                            photo=File(photo_file, name=photo_filename))
                user.set_password('password')
                user.save()
                users.append(user)
    User.objects.bulk_create(users)


def generate_word():
    with open('english_dictionary.txt') as f:
        words = f.readlines()
    words = [word.strip() for word in words]
    return random.choice(words)


def generate_tags(num):
    tags = []
    for i in range(num):
        name = generate_word()
        if not Tag.objects.with_name(name).exists():
            tag = Tag.objects.create(name=name)
            tags.append(tag)
    Tag.objects.bulk_create(tags)


def generate_marks(num):
    STATUS_CHOICES = [
        ('l', 'like'),
        ('d', 'dislike'),
    ]
    marks = []
    for i in range(num):
        status = random.choice(STATUS_CHOICES)
        to_user = User.objects.random()
        from_user = None
        while from_user is None or from_user.name == to_user.name:
            from_user = User.objects.random()
        mark = Mark.objects.create(to_user=to_user, from_user=from_user, status=status[0])
        marks.append(mark)
    Tag.objects.bulk_create(marks)


def generate_questions(num):
    questions = []
    for i in range(num):
        title = f'Question {str(random.randint(1, 2000000))}'
        if not Question.objects.with_title(title).exists():
            text = ' '.join(random.choices(corpus, k=100))
            author = User.objects.random()
            tag = [Tag.objects.random(), Tag.objects.random()]
            question = Question.objects.create(title=title, text=text, author=author, tag=tag)
            questions.append(question)
    Question.objects.bulk_create(questions)


def generate_answers(num):
    #TODO
    tags = []
    for i in range(num):
        name = generate_word()
        if not Tag.objects.with_name(name).exists():
            tag = Tag(name=name)
            tag.save()
            tags.append(tag)
    Tag.objects.bulk_create(tags)


def fill_db(num):
    generate_tags(num)
    generate_users(num)
    generate_marks(200*num)
    #generate_questions(10*num)
    #generate_answers(100*num)


if __name__ == '__main__':
    User.objects.all().delete()
    Tag.objects.all().delete()
    Mark.objects.all().delete()
    Question.objects.all().delete()
    Answer.objects.all().delete()

    reset_sequence('Users')
    reset_sequence('Tags')
    reset_sequence('Marks')
    reset_sequence('Questions')
    reset_sequence('Answers')

    num = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    #fill_db(num)
