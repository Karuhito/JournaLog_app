from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from .base import BaseUpdateView
from django.shortcuts import render, get_object_or_404, redirect
from journal.models import Journal, Reflection
from journal.forms import ReflectionForm
from datetime import date

class CreateReflectionView(LoginRequiredMixin, View):
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
                "journal:journal_detail",
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            'journal': journal,
            'form': form,
        })
    
class UpdateReflectionView(LoginRequiredMixin, BaseUpdateView):
    model = Reflection
    form_class = ReflectionForm
    title = "振り返り編集"
    header_class = "bg-warning"
    template_name = "journal/reflection_update.html"