import uuid

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import Course, Module, TheoryContent, Question, AnswerOption, UserProgress, UserAnswer
from .forms import CourseForm, ModuleForm, TheoryContentForm, QuestionForm, AnswerOptionFormSet


def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    modules = course.modules.filter(is_hidden=False) if not is_teacher(request.user) else course.modules.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'is_teacher': is_teacher(request.user)
   })


@login_required
def module_theory(request, module_id):
    module = get_object_or_404(Module, id=module_id, module_type='theory')
    theory_content = get_object_or_404(TheoryContent, module=module)
    return render(request, 'courses/module_theory.html', {
        'module': module,
        'theory_content': theory_content,
        'is_teacher': is_teacher(request.user)
    })


@login_required
def module_test(request, module_id):
    module = get_object_or_404(Module, pk=module_id, module_type='test')
    questions = module.questions.all().prefetch_related('options')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            if question.question_type == 'text':
                answer_text = request.POST.get(f'question_{question.id}', '')
                is_correct = answer_text.lower() == question.options.filter(is_correct=True).first().text.lower()

                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    answer_text=answer_text,
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

            elif question.question_type in ['single', 'multiple']:
                selected_ids = request.POST.getlist(f'question_{question.id}')
                correct_options = question.options.filter(is_correct=True)
                selected_options = question.options.filter(id__in=selected_ids)

                is_correct = set(correct_options.values_list('id', flat=True)) == set(selected_ids)

                user_answer = UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    is_correct=is_correct
                )
                user_answer.selected_options.set(selected_options)

                if is_correct:
                    score += 1

            # TODO: Additional logic for other questions

        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            module=module
        )
        progress.score = int((score / total) * 100) if total > 0 else 0
        progress.completed = True
        progress.save()

        messages.success(request, f'Тест завершен! Ваш результат: {progress.score}%')
        return redirect('module_test', module_id=module.id)

    return render(request, 'courses/module_test.html', {
        'module': module,
        'questions': questions,
        'is_teacher': is_teacher(request.user)
    })


# @user_passes_test(is_teacher)
def edit_theory(request, module_id):
    module = get_object_or_404(Module, pk=module_id, module_type='theory')
    theory_content, created = TheoryContent.objects.get_or_create(module=module)

    if request.method == 'POST':
        form = TheoryContentForm(request.POST, request.FILES, instance=theory_content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Теоретический материал успешно обновлен!')
            return redirect('module_theory', module_id=module.id)
    else:
        form = TheoryContentForm(instance=theory_content)

    return render(request, 'courses/edit_theory.html', {
        'module': module,
        'form': form
    })


# @user_passes_test(is_teacher)
def edit_questions(request, module_id):
    module = get_object_or_404(Module, pk=module_id, module_type='test')

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question = get_object_or_404(Question, pk=question_id, module=module)
            form = QuestionForm(request.POST, instance=question)
        else:
            form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.module = module
            question.save()

            formset = AnswerOptionFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Вопрос успешно сохранен!')
                return redirect('edit_questions', module_id=module.id)
    else:
        form = QuestionForm()

    questions = module.questions.all().prefetch_related('options')
    return render(request, 'courses/edit_questions.html', {
        'module': module,
        'questions': questions,
        'form': form
    })


# @user_passes_test(is_teacher)
def toggle_module(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    module.is_hidden = not module.is_hidden
    module.save()

    messages.success(request, f'Модуль {"скрыт" if module.is_hidden else "отображен"}!')
    return redirect('course_detail', pk=module.course.id)