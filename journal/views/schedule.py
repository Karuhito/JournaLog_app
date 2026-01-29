from django.urls import reverse
from .base import *
from ..models import Schedule
from ..forms import ScheduleForm, ScheduleFormSet

class CreateScheduleView(BaseCreateView):
    model = Schedule
    formset_class = ScheduleFormSet
    prefix = "schedule"
    allow_multiple = True
    template_name = "journal/create_schedule.html"

class UpdateScheduleView(BaseUpdateView):
    model = Schedule
    form_class = ScheduleForm
    title = "Scheduleの編集"
    feature = "schedule"
    template_name = "journal/update_schedule.html"

class DeleteScheduleView(BaseDeleteView):
    model = Schedule
    object_name = "Schedule"