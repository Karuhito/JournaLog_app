from django.urls import reverse
from .base import BaseCreateView, BaseDeleteView, BaseUpdateView
from ..models import Goal
from ..forms import GoalFormSet, GoalForm

class CreateGoalView(BaseCreateView):
    model = Goal
    formset_class = GoalFormSet
    prefix = "goal"
    allow_multiple = True
    template_name = "journal/create_goal.html"

class UpdateGoalView(BaseUpdateView):
    model = Goal
    form_class = GoalForm
    title = "Goalの編集"
    feature = "goal"
    template_name = "journal/update_goal.html"


class DeleteGoalView(BaseDeleteView):
    model = Goal
    object_name = "Goal"
    model_label = "Goal"



    


