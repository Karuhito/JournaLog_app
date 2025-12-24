from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, DetailView, CreateView, DeleteView, UpdateView,)
from .models import Journal, Todo, Goal
from datetime import date, datetime, timedelta
import calendar
from .forms import GoalFormSet, TodoFormSet

# Home画面のView
class HomeScreenView(LoginRequiredMixin,TemplateView):
    template_name = 'journal/home.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        # 年・月プルダんリストの生成
        context['years'] = [y for y in range(today.year -2, today.year +5)]
        context['months'] = [m for m in range(1,13)]
        context['year'] = year
        context['month'] = month
        context['today'] = today

        # カレンダーの生成
        cal = calendar.Calendar(firstweekday=6) # 日曜日始まり
        month_days = cal.monthdatescalendar(year, month) # 週ごとの日付リスト

        # 日付ごとの journal 存在フラグ
        journal_dates = Journal.objects.filter(
            user=self.request.user,
            date__year=year,
            date__month=month
        ).prefetch_related('goal_set','todo_set')

        journal_map = {
            j.date: (j.goal_set.exists() or j.todo_set.exists())
            for j in journal_dates
        }

        # カレンダーデータの構築
        cal_data = []
        for week in month_days:
            week_data = []
            for day in week:
                week_data.append({
                    'day': day,
                    'has_journal': journal_map.get(day, False),
                })
            cal_data.append(week_data)

        context.update({
            'year': year,
            'month': month,
            'cal_data': cal_data,
        })
        return context
    
# Journal関連のView
class JournalDetailView(DetailView): # その日のGoalとTodoを表示するView
    template_name = 'journal/journal_detail.html'
    model = Journal
    
    def get_context_data(self, **kwargs):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']

        return get_object_or_404(
            Journal,
            user=self.request.user,
            date=date(year, month, day)
        )
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        journal = self.object

        goals = journal.goal_set.all()
        todos = journal.todo_set.all()

        if not goals.exists() and not todos.exists():
            return redirect(
                'journal_init',
                year=journal.date.year,
                month=journal.date.month,
                day=journal.date.day
            )
        
        context = self.get_context_data(object=journal)
        context['goals'] = goals
        context['todos'] = todos
        return self.render_to_response(context)
    
class JournalInitView(CreateView):
    template_name = 'journal/journal_init.html'
    def get(self, request, year, month, day):
        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=date(year, month, day)
        )

        goal_formset = GoalFormSet(queryset=journal.goal_set.none())
        todo_formset = TodoFormSet(queryset=journal.todo_set.none())

        return render(request, self.template_name, {
            'goal_formset': goal_formset,
            'todo_formset': todo_formset,
            'journal': journal,
        })
    
    def post(self, request, year, month, day):
        journal = get_object_or_404(
            Journal,
            user = request.user,
            date = date(year, month, day)
        )

        goal_formset = GoalFormSet(request.POST, queryset=journal.goal_set.none())
        todo_formset = TodoFormSet(request.POST, queryset=journal.todo_set.none())

        if goal_formset.is_valid() and todo_formset.is_valid():
            goal = goal_formset.save(commit=False)
            todo = todo_formset.save(commit=False)

            for goal in goal:
                if not goal.title:
                    continue
                goal.journal = journal
                goal.save()
            
            for todo in todo:
                if not todo.title:
                    continue
                todo.journal = journal
                todo.save()

            return redirect('journal_detail', year=year, month=month, day=day)
        
        return render(request, self.template_name,{
            'goal_formset': goal_formset,
            'todo_formset': todo_formset,
            'journal': journal,
        })

# Goal関連のView
class CreateGoalView(CreateView):
    template_name = 'journal/create_goal.html'
    model = Goal
    fields = ('title',)
    success_url = reverse_lazy('journal:journal_detail', kwargs={
        'year': 'year',
        'month': 'month',
        'day': 'day',
        })
    
    def form_valid(self, form):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']

        from datetime import date
        
        journal_date = date(year, month, day)

        journal = get_object_or_404(
            Journal,
            user=self.request.user,
            date=journal_date
            ) 
        form.instance.journal = journal

        return super().form_valid(form)
        

class UpdateGoalView(UpdateView):
    template_name = 'journal/update_goal.html'
    model = Goal

    def get_queryset(self):
        return Goal.objects.filter(journal__user=self.request.user)

class DeleteGoalView(DeleteView):
    template_name = 'journal/delete_goal.html'
    model = Goal
    success_url = reverse_lazy('accounts:home')

    def get_queryset(self):
        return Goal.objects.filter(journal__user=self.request.user)


# Todo関連のView
class CreateTodoView(CreateView):
    template_name = 'journal/create_todo.html'
    model = Todo
    fields = ('title','start_time','end_time')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        journal_date = date(
            int(self.kwargs['year']),
            int(self.kwargs['month']),
            int(self.kwargs['day'])
        )
        journal = get_object_or_404(
            Journal,
            user=self.request.user,
            date=journal_date
        )
        form.instance.journal = journal
        return super().form_valid(form)

class UpdateTodoView(UpdateView):
    template_name = 'journal/update_todo.html'
    model = Todo
    fields = ('title','start_time','end_time','is_done')

    def get_queryset(self):
        return Todo.objects.filter(journal__user=self.request.user)

class DeleteTodoView(DeleteView):
    template_name = 'journal/delete_todo.html'
    model = Todo
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Todo.objects.filter(journal__user=self.request.user)



