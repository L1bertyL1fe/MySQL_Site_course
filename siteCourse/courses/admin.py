from django.contrib import admin
from .models import Course, Module, TheoryContent, Question, AnswerOption, UserProgress, UserAnswer

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(TheoryContent)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOption)
admin.site.register(UserProgress)
admin.site.register(UserAnswer)