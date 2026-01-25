from django.urls import reverse
from .base import BaseCreateView, BaseDeleteView, BaseUpdateView
from django.views import View
from ..models import Todo
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
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

class TodoToggleView(View):
    def post(self, request, pk):
        todo = get_object_or_404(
            Todo,
            pk=pk,
            journal__user=request.user
        )

        todo.is_done = not todo.is_done
        todo.save()

        return JsonResponse({
            "success": True,
            "is_done": todo.is_done,
        })

