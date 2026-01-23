from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView
from journal.models import Journal
from journal.forms import GoalFormSet, TodoFormSet
from datetime import timedelta

class JournalOverView(LoginRequiredMixin, DetailView):
    model = Journal
    template_name = 'journal/journal_over.html'

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    # --------------------
    # Journal取得（存在しなければ None）
    # --------------------
    def get_object(self, queryset=None):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']

        return Journal.objects.filter(
            user=self.request.user,
            date=date(year, month, day)
        ).first()

    # --------------------
    # 存在しない or 空なら Init へ
    # --------------------
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # 🔴 Journalが存在しない
        if self.object is None:
            return redirect(
                'journal:journal_init',
                year=kwargs['year'],
                month=kwargs['month'],
                day=kwargs['day']
            )

        # 🔴 Journalはあるが中身が空
        if (
            not self.object.goals.exists()
            and not self.object.todos.exists()
            and not self.object.schedules.exists()
            and not self.object.reflection.exists()
        ):
            return redirect(
                'journal:journal_init',
                year=self.object.date.year,
                month=self.object.date.month,
                day=self.object.date.day
            )

        return super().get(request, *args, **kwargs)

    # --------------------
    # context
    # --------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journal = self.object

        context['goals'] = journal.goals.all()
        context['todos'] = journal.todos.all()
        context['schedules'] = journal.schedules.order_by("start_time")
        context['reflection'] = journal.reflection.first()
        context['journal_date'] = journal.date
        context['prev_day'] = journal.date - timedelta(days=1)
        context['next_day'] = journal.date + timedelta(days=1)

        return context
    
class JournalInitView(LoginRequiredMixin, View):
    template_name = 'journal/journal_init.html'
    login_url = 'accounts:login'


    def get(self, request, year, month, day):
        journal_date = date(year, month, day)

        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=journal_date
        )

        context = {
            "journal": journal,
            "goal_formset": GoalFormSet(queryset=journal.goals.none(), prefix="goal"),
            "todo_formset": TodoFormSet(queryset=journal.todos.none(), prefix="todo"),
            "prev_day": journal_date - timedelta(days=1),
            "next_day": journal_date + timedelta(days=1),
            "journal_date": journal_date,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, year, month, day):
        journal = get_object_or_404(
        Journal,
        user=request.user,
        date=date(year, month, day)
        )

        goal_formset = GoalFormSet(
            request.POST,
            queryset=journal.goals.none(),
            prefix="goal"
        )
        todo_formset = TodoFormSet(
            request.POST,
            queryset=journal.todos.none(),
            prefix="todo"
        )

        if goal_formset.is_valid() and todo_formset.is_valid():
            goals = goal_formset.save(commit=False)
            todos = todo_formset.save(commit=False)

            for goal in goals:
                if goal.title:
                    goal.journal = journal
                    goal.save()

            for todo in todos:
                if todo.title:
                    todo.journal = journal
                    todo.save()

            return redirect(
                "journal:journal_over",
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            "goal_formset": goal_formset,
            "todo_formset": todo_formset,
            "journal": journal,
        })
