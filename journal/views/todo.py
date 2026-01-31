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
    allow_multiple = True
    template_name = "journal/create_todo.html"


class UpdateTodoView(BaseUpdateView):
    model = Todo
    form_class = TodoUpdateForm
    title = "Todoの編集"
    template_name = "journal/update_todo.html"
    feature = "todo"

class DeleteTodoView(BaseDeleteView):
    model = Todo
    object_name = "Todo"
    feature = "todo"
    template_name = "journal/delete_todo.html"

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

