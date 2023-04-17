from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class QuestionManager(models.Manager):
    def with_tag(self, tag):
        return self.filter(tag__name=tag)

    def with_title(self, title):
        return self.filter(title=title)

    def with_id(self, id):
        return self.filter(id=id)

    def random(self):
        return self.order_by('?').first()


class TagManager(models.Manager):
    def with_name(self, name):
        return self.filter(name=name)

    def random(self):
        return self.order_by('?').first()


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным электронным адресом и паролем.
        """
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанными электронным адресом и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_populars(self):
        return self.filter(rating=1)

    def with_email(self, email):
        return self.filter(email=email)

    def random(self):
        return self.order_by('?').first()


class MarkManager(models.Manager):
    pass


class AnswerManager(models.Manager):
    def to_question(self, question_title):
        return self.filter(to_question=question_title)


class Answer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    to_question = models.ForeignKey('Question', on_delete=models.CASCADE,
                                    related_name='answer_to_question',
                                    verbose_name='answer2question')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='answer_author',
                               verbose_name='answer_author')
    text = models.CharField(max_length=3000, verbose_name='answer_text')
    STATUS_CHOICES = [
        ('r', 'right'),
        ('u', 'unknown')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='answer_status',
                              default=STATUS_CHOICES[-1])

    class Meta:
        db_table = 'answers'

    objects = AnswerManager()

    def __str__(self):
        return f'{self.author}'


class Question(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='question_title')
    text = models.CharField(max_length=3000, verbose_name='question_text')
    author = models.ForeignKey('User', on_delete=models.CASCADE,
                               related_name='author_of_question', verbose_name='question_author')
    tag = models.ManyToManyField('Tag', related_name='questions', verbose_name='question_tag')

    class Meta:
        db_table = 'questions'

    objects = QuestionManager()

    def get_id(self):
        return self.id

    def __str__(self):
        return self.title


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, blank=True, verbose_name='user_name')
    email = models.EmailField(unique=True, verbose_name='email')
    rating = models.IntegerField(verbose_name='rating')
    photo = models.ImageField(upload_to='./static/img/user_avatars', blank=True, null=True,
                              verbose_name='user_photo')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='registration_date')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.id} {self.name}'

    objects = UserManager()


class Tag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='tag_name')

    class Meta:
        db_table = 'tags'

    objects = TagManager()

    def __str__(self):
        return f'{self.name}'


class Mark(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='marks_received',
                                verbose_name='recipient')
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='marks_given',
                                  verbose_name='sandler')
    STATUS_CHOICES = [
        ('l', 'like'),
        ('d', 'dislike'),
    ]
    name = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='mark_type')

    class Meta:
        db_table = 'marks'

    objects = MarkManager()

    def __str__(self):
        return f'{self.to_user} {self.name}'
