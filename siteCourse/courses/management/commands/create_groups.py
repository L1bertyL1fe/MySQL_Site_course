from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Module, TheoryContent, Question


class Command(BaseCommand):
    help = 'Creates default user groups with permissions'

    def handle(self, *args, **options):
        # Группа преподавателей
        teacher_group, created = Group.objects.get_or_create(name='Teachers')

        # Добавляем разрешения
        content_types = ContentType.objects.get_for_models(Course, Module, TheoryContent, Question)

        permissions = Permission.objects.filter(
            content_type__in=content_types.values(),
            codename__in=[
                'add_course', 'change_course', 'delete_course',
                'add_module', 'change_module', 'delete_module',
                'add_theorycontent', 'change_theorycontent', 'delete_theorycontent',
                'add_question', 'change_question', 'delete_question',
            ]
        )

        teacher_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Successfully created teacher group with permissions'))