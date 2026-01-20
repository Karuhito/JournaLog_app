from django.urls import reverse
from .base import BaseCreateView, BaseDeleteView, BaseUpdateView
from ..models import Todo
from ..forms import TodoUpdateForm, TodoFormSet

class CreateTodoView(BaseCreateView):
    model = Todo
    formset_class = TodoFormSet
    prefix = "todo"
    template_name = "journal/todo_create.html"


class UpdateTodoView(BaseUpdateView):
    model = Todo
    form_class = TodoUpdateForm
    title = "Todoの編集"
    header_class = "bg-info"
    template_name = "journal/todo_update.html"

class DeleteTodoView(BaseDeleteView):
    model = Todo
    object_name = "Todo"
