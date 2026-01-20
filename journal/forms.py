import datetime
from django import forms
from .models import Goal, Todo, Schedule, Reflection
from django.forms import modelformset_factory

# 時間の選択肢を10分刻みで生成（valueも文字列）
def time_choices(interval=15):
    choices = []
    for hour in range(0, 24):
        for minute in range(0, 60, interval):
            time_obj = datetime.time(hour, minute)
            label = f"{hour:02d}:{minute:02d}"
            choices.append((time_obj, label))
    return choices

# Goalフォーム
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title']
        labels = {
            'title': '今日の目標',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Todoフォーム
class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        labels = {
            'title': '今日やることの内容',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Todo内容'
                }
            ),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_done']
        labels = {
            'title': 'やること',
            'is_done': '完了',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'is_done': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }


# Scheduleフォーム
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'start_time', 'end_time',]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '予定内容',
            }),
            'start_time': forms.Select(
                choices=time_choices(15),
                attrs={
                'class': "form-select time-select"
            }),
            "end_time": forms.Select(
                choices=time_choices(15),                
                attrs={  
                'class': "form-select time-select"
            }),
        }

# Reflection フォーム
class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['content']
        labels = {
            'content':'今日の振り返り',
            }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '今日の振り返りを入力してください',
                    'rows':5, # 初期表示行数を設定
                }
            ),
        }

# フォームセット
GoalFormSet = modelformset_factory(
    Goal,
    form=GoalForm,
    extra=1,
    can_delete=False
    )

TodoFormSet = modelformset_factory(
    Todo,
    form=TodoCreateForm,
    extra=1,
    can_delete=False
    )

ScheduleFormSet = modelformset_factory(
    Schedule,
    form=ScheduleForm,
    extra=1,
    can_delete=False
    )