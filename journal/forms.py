import datetime
import django.forms as forms
from .models import Goal, Todo
from django.forms import modelformset_factory

def time_choices(interval=10):
    choices = [('', '---')]
    for hour in range(0, 24):
        for minute in range(0, 60, interval):
            time = datetime.time(hour, minute)
            label = f"{hour:02d}:{minute:02d}"
            choices.append((time, label))
    return choices

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title',]

class TodoForm(forms.ModelForm):
    start_time = forms.ChoiceField(
        label='開始時刻',
        choices=time_choices(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    end_time = forms.ChoiceField(
        label='終了時刻',
        choices=time_choices(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Todo
        fields = ['title', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Todo内容'
            }),
        }

GoalFormSet = modelformset_factory(
    Goal,
    form=GoalForm,
    extra=3,
    can_delete=False
)

TodoFormSet = modelformset_factory(
    Todo,
    form=TodoForm,
    extra=5,
    can_delete=False
)