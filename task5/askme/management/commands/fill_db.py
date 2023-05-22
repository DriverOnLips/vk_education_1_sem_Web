import os
import sys
import random
import nltk
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import connections
from askme.models import Question, User, Tag, Mark2Question, Mark2Answer, Answer


class Command(BaseCommand):
    help = 'Fill the database with random data'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int, nargs='?', default=100)

    def handle(self, *args, **options):
        num = options['num']
        nltk.download('gutenberg')
        corpus = nltk.corpus.gutenberg.words()
        words_dict = [word.lower() for word in corpus if len(word) >= 4]


        def reset_sequence(table_name):
            with connections['default'].cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), coalesce(max(id), 0) + 1, false) FROM {table_name};")


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
            photos_dir = "media/photos"

            for i in range(num):
                name = random.choice(names) + ' ' + random.choice(surnames)
                email = f'{name.lower().replace(" ", ".")}{str(random.randint(1, 9999))}' \
                        f'@{random.choice(domains)}'
                if not User.objects.with_email(email).exists():
                    photo_filenames = [f for f in os.listdir(photos_dir) if
                                       os.path.isfile(os.path.join(photos_dir, f)) and f.lower().
                                       endswith(tuple(image_extensions))]
                    photo_filename = random.choice(photo_filenames)
                    with open(os.path.join(photos_dir, photo_filename), "rb") as photo_file:
                        photo_content = photo_file.read()
                        photo = ContentFile(photo_content, photo_filename)
                        user = User(email=email, name=name, photo=photo)
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


        def generate_marks2question(num):
            STATUS_CHOICES = [
                ('l', 'like'),
                ('d', 'dislike'),
            ]
            marks = []
            for i in range(num):
                name = random.choice(STATUS_CHOICES)
                to_question = Question.objects.random()
                from_user = User.objects.random()
                mark = Mark2Question(to_question=to_question, from_user=from_user, name=name[0])
                marks.append(mark)
            Mark2Question.objects.bulk_create(marks)


        def generate_marks2answer(num):
            STATUS_CHOICES = [
                ('l', 'like'),
                ('d', 'dislike'),
            ]
            marks = []
            for i in range(num):
                name = random.choice(STATUS_CHOICES)
                to_answer = Answer.objects.random()
                from_user = User.objects.random()
                mark = Mark2Answer(to_answer=to_answer, from_user=from_user, name=name[0])
                marks.append(mark)
            Mark2Answer.objects.bulk_create(marks)


        def generate_questions(num):
            questions = []
            for i in range(num):
                title = f'Question {str(random.randint(1, 2000000))}'
                if not Question.objects.with_title(title).exists():
                    text = ' '.join(random.choices(words_dict, k=40))
                    author = User.objects.random()
                    rating = random.randint(-100, 100)
                    question = Question(title=title, text=text, author=author, rating=rating)
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
                rating = random.randint(-100, 100)
                answer = Answer(to_question=to_question, author=author, text=text, status=status[0],
                                rating=rating)
                answers.append(answer)
            Answer.objects.bulk_create(answers)


        def fill_db(num):
            generate_users(num)
            generate_tags(num)
            generate_questions(10 * num)
            generate_answers(100 * num)
            generate_marks2question(200*num)
            generate_marks2answer(200*num)

        User.objects.all().delete()
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Mark2Question.objects.all().delete()
        Mark2Answer.objects.all().delete()

        reset_sequence('Tags')
        reset_sequence('Users')
        reset_sequence('Questions')
        reset_sequence('Answers')
        reset_sequence('marks2questions')
        reset_sequence('marks2answers')

        fill_db(num)
