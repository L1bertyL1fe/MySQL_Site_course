# Generated by Django 5.2 on 2025-04-18 16:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('module_type', models.CharField(choices=[('theory', 'Теоретический модуль'), ('test', 'Тестирование')], max_length=10)),
                ('is_hidden', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('text', 'Текстовый ответ'), ('single', 'Выбор одного варианта'), ('multiple', 'Выбор нескольких вариантов'), ('match', 'Соответствие')], max_length=10)),
                ('text', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('match_value', models.CharField(blank=True, max_length=200, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='TheoryContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='theory_images/')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('animation', models.FileField(blank=True, null=True, upload_to='theory_animations/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='theory_audio/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('module', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='theory_content', to='courses.module')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
                ('selected_options', models.ManyToManyField(blank=True, to='courses.answeroption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('last_attempt', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'module')},
            },
        ),
    ]
