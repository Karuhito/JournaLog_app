from django.urls import reverse
from django.views import View
from .base import BaseUpdateView
from django.shortcuts import render, get_object_or_404, redirect
from journal.models import Journal, Reflection
from journal.forms import ReflectionForm
from datetime import date, timezone

class CreateReflectionView(View):
    template_name = "journal/reflection_create.html"
    login_url = "accounts:login"

    def get(self, request, year, month, day):
        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=date(year, month, day)
        )

        form = ReflectionForm()
        return render(request, self.template_name, {
            'journal': journal,
            'form': form,
        })

    def post(self, request, year, month, day):
        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=date(year, month, day)
        )

        form = ReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.journal = journal
            reflection.save()
            return redirect(
                "journal:journal_over",
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            'journal': journal,
            'form': form,
        })
    
class UpdateReflectionView(BaseUpdateView):
    model = Reflection
    form_class = ReflectionForm
    title = "振り返り編集"
    header_class = "bg-warning"
    template_name = "journal/reflection_update.html"

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