from django import forms
from .models import Course, Module, TheoryContent, Question, AnswerOption

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'module_type', 'is_hidden', 'order']

class TheoryContentForm(forms.ModelForm):
    class Meta:
        model = TheoryContent
        fields = ['text', 'image', 'video_url', 'animation', 'audio']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'text', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['text', 'is_correct', 'match_value']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

AnswerOptionFormSet = forms.inlineformset_factory(
    Question, AnswerOption, form=AnswerOptionForm, extra=1, can_delete=True
)