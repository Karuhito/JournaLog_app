from django.urls import reverse
from .base import *
from ..models import Schedule
from ..forms import ScheduleForm, ScheduleFormSet

class CreateScheduleView(BaseCreateView):
    model = Schedule
    formset_class = ScheduleFormSet
    prefix = "schedule"
    template_name = "journal/schedule_create.html"

class UpdateScheduleView(BaseUpdateView):
    model = Schedule
    form_class = ScheduleForm
    title = "Scheduleの編集"
    header_class = "bg-success"
    template_name = "journal/schedule_update.html"

class DeleteScheduleView(BaseDeleteView):
    model = Schedule
    object_name = "Schedule"