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
            user_correct = False
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

                is_correct = set(correct_options.values_list('id', flat=True)) == set(map(int,selected_ids))
                user_answer = UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    is_correct=is_correct
                )
                user_answer.selected_options.set(selected_options)

                if is_correct:
                    score += 1

            elif question.question_type == 'match':
                # Получаем выбранные пользователем пары
                user_pairs = []
                pair_index = 0
                while True:
                    term_id = request.POST.get(f'question_{question.id}_term_{pair_index}')
                    definition_value = request.POST.get(f'question_{question.id}_definition_{pair_index}')
                    if not term_id or not definition_value:
                        break
                    user_pairs.append((
                        int(term_id),
                        definition_value.strip().lower()
                    ))
                    pair_index += 1

                # Получаем правильные пары из базы
                correct_pairs = {
                    opt.id: opt.match_value
                    for opt in question.options.all()
                }

                # Проверяем каждую пару
                correct_count = 0
                for term_id, definition_id in user_pairs:
                    if str(correct_pairs.get(term_id, '')).lower() == str(definition_id).lower():
                        correct_count += 1
                # Считаем ответ правильным если все пары верные
                is_correct = correct_count == len(correct_pairs)

                if is_correct:
                    score += 1

                # Сохраняем ответ
                user_answer = UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    is_correct=is_correct
                )

                # Сохраняем выбранные пары
                for term_id, definition_id in user_pairs:
                    option = AnswerOption.objects.get(id=term_id)
                    user_answer.selected_options.add(option)

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

    if 'delete_question' in request.GET:
        question_id = request.GET['delete_question']
        question = get_object_or_404(Question, id=question_id, module=module)
        question.delete()
        messages.success(request, 'Вопрос успешно удален!')
        return redirect('edit_questions', module_id=module.id)

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question_type = request.POST.get('question_type')
        question_text = request.POST.get('question_text')

        # Создаем или получаем вопрос
        if question_id and question_id != 'new':
            question = get_object_or_404(Question, pk=question_id, module=module)
        else:
            question = Question(module=module)

        question.question_type = question_type
        question.text = question_text
        question.save()

        # Обрабатываем варианты ответов
        options_data = {}
        for key in request.POST:
            if key.startswith('options['):
                parts = key.split('[')
                option_id = parts[1].split(']')[0]
                field = parts[2].split(']')[0]

                if option_id not in options_data:
                    options_data[option_id] = {}
                options_data[option_id][field] = request.POST[key]

        # Удаляем старые варианты
        question.options.all().delete()

        print("мы здесь!!!")
        print(question_type)

        if question.question_type == 'text':
            correct_answer = request.POST.get('correct_answer')
            answer_option = AnswerOption(
                question=question,
                text=correct_answer,
                is_correct=True
            )
            answer_option.save()

        # Создаем новые варианты
        for option_id, data in options_data.items():
            # Для других типов вопросов
            answer_option = AnswerOption(
                question=question,
                text=data.get('text', ''),
                match_value=data.get('match_value', ''),
                is_correct=False
            )

            # Определяем правильные ответы
            if question.question_type == 'single':
                answer_option.is_correct = (request.POST.get('correct_option') == option_id)
            elif question.question_type == 'multiple':
                answer_option.is_correct = option_id in request.POST.getlist('correct_options[]')

            answer_option.save()

        messages.success(request, 'Вопрос успешно сохранен!')
        return redirect('edit_questions', module_id=module.id)

    questions = module.questions.all().prefetch_related('options')
    return render(request, 'courses/edit_questions.html', {
        'module': module,
        'questions': questions
    })


# @user_passes_test(is_teacher)
def toggle_module(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    module.is_hidden = not module.is_hidden
    module.save()

    messages.success(request, f'Модуль {"скрыт" if module.is_hidden else "отображен"}!')
    return redirect('course_detail', pk=module.course.id)