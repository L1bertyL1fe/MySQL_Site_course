import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class Roles(models.TextChoices):
        STUDENT = 'student', 'студент'
        TEACHER = 'teacher', 'преподователь'
        ADMIN = 'admin', 'админ'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )

    def __str__(self):
        return self.username

    def is_student(self):
        return self.role == self.Roles.STUDENT

    def is_teacher(self):
        return self.role == self.Roles.TEACHER

    def is_admin(self):
        return self.role == self.Roles.ADMIN

