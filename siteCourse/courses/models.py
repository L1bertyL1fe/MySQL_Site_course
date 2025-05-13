import uuid

from django.db import models

# Create your models here.
from users.models import CustomUser as User
from django.utils import timezone
from django.urls import reverse

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})

class Module(models.Model):
    MODULE_TYPES = (
        ('theory', 'Теоретический модуль'),
        ('test', 'Тестирование'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    module_type = models.CharField(max_length=10, choices=MODULE_TYPES)
    is_hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.get_module_type_display()})"

class TheoryContent(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='theory_content')
    text = models.TextField()
    image = models.ImageField(upload_to='theory_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    animation = models.FileField(upload_to='theory_animations/', blank=True, null=True)
    audio = models.FileField(upload_to='theory_audio/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Теория для {self.module.title}"

class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'Текстовый ответ'),
        ('single', 'Выбор одного варианта'),
        ('multiple', 'Выбор нескольких вариантов'),
        ('match', 'Соответствие'),
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text[:50]}... ({self.get_question_type_display()})"

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    match_value = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.text} {'(верный)' if self.is_correct else ''}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    selected_options = models.ManyToManyField(AnswerOption, blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def check_match_answer(self):
        if self.question.question_type != 'match':
            return False

        correct_pairs = {
            opt.id: opt.match_value
            for opt in self.question.options.all()
        }

        user_pairs = [
            (opt.id, opt.match_value)
            for opt in self.selected_options.all()
        ]

        return all(
            str(correct_pairs.get(term_id, '')) == str(definition_id)
            for term_id, definition_id in user_pairs
        )

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:50]}..."