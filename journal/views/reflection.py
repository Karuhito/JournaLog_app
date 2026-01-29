from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from .base import BaseUpdateView
from django.shortcuts import render, get_object_or_404, redirect
from journal.models import Journal, Reflection
from journal.forms import ReflectionForm
from datetime import date, timezone

class CreateReflectionView(LoginRequiredMixin, CreateView):
    model = Reflection
    form_class = ReflectionForm
    template_name = "journal/create_reflection.html"

    def dispatch(self, request, *args, **kwargs):
        self.journal_date = date(
            int(kwargs["year"]),
            int(kwargs["month"]),
            int(kwargs["day"]),
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        journal = get_object_or_404(
            Journal,
            user=self.request.user,
            date=self.journal_date
        )
        form.instance.journal = journal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "journal:journal_over",
            kwargs={
                "year": self.journal_date.year,
                "month": self.journal_date.month,
                "day": self.journal_date.day,
            }
        )
    
class UpdateReflectionView(BaseUpdateView):
    model = Reflection
    form_class = ReflectionForm
    title = "振り返り編集"
    template_name = "journal/update_reflection.html"
    feature = "reflection"

    def get_success_url(self):
        # journal が None の場合は安全にホームに戻す
        journal = getattr(self.object, 'journal', None)
        if journal:
            return reverse(
                "journal:journal_over",
                kwargs={
                    "year": journal.date.year,
                    "month": journal.date.month,
                    "day": journal.date.day,
                }
            )
        else:
            return reverse("journal:home")