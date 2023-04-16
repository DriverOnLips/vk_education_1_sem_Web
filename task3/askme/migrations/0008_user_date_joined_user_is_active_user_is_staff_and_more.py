# Generated by Django 4.1.7 on 2023-04-15 06:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0007_alter_answer_id_alter_mark_id_alter_question_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата регистрации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_author', to='askme.user', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='to_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_to_question', to='askme.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='./static/img/user_avatars', verbose_name='Фото пользователя'),
        ),
    ]