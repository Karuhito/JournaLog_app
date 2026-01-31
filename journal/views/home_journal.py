from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView
from journal.models import Journal, Goal, Todo, Schedule, Reflection
from journal.forms import GoalFormSet, TodoFormSet


# =========================
# HomeScreenView（カレンダー表示）
# =========================
class HomeScreenView(LoginRequiredMixin, TemplateView):
    template_name = "journal/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        view_mode = self.request.GET.get("view", "month")
        context["view_mode"] = view_mode
        context["today"] = today

        if view_mode == "month":
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))

            import calendar
            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdatescalendar(year, month)

            # 今月のジャーナルを取得
            journals = Journal.objects.filter(
                user=self.request.user,
                date__year=year,
                date__month=month
            ).prefetch_related("goals", "todos", "schedules", "reflection")

            # 日付: 記録あり(True/False) の辞書を作成
            journal_map = {
                j.date: (
                    j.goals.exists() or
                    j.todos.exists() or
                    j.schedules.exists() or
                    j.reflection.exists()
                )
                for j in journals
            }

            cal_data = []
            for week in month_days:
                week_row = []
                for day in week:
                    week_row.append({
                        "day": day,
                        "is_today": day == today,
                        "is_other_month": day.month != month,
                        "has_journal": journal_map.get(day, False),  # 🔹追加
                        "url": f"/journal/{day.year}/{day.month}/{day.day}/"
                    })
                cal_data.append(week_row)

            context.update({
                "year": year,
                "month": month,
                "years": [y for y in range(today.year - 2, today.year + 5)],
                "months": list(range(1, 13)),
                "cal_data": cal_data,
            })

        else:  # 週表示
            week_start_str = self.request.GET.get("week_start")
            if week_start_str:
                week_start = date.fromisoformat(week_start_str)
            else:
                week_start = today - timedelta(days=today.weekday())

            week_end = week_start + timedelta(days=6)

            journals = Journal.objects.filter(
                user=self.request.user,
                date__range=(week_start, week_end)
            ).prefetch_related("goals", "todos", "schedules", "reflection")

            # 日付: 記録あり(True/False) の辞書
            journal_map = {
                j.date: (
                    j.goals.exists() or
                    j.todos.exists() or
                    j.schedules.exists() or
                    j.reflection.exists()
                )
                for j in journals
            }

            week_data = []
            for i in range(7):
                day = week_start + timedelta(days=i)
                week_data.append({
                    "day": day,
                    "is_today": day == today,
                    "has_journal": journal_map.get(day, False),  # 🔹追加
                    "url": f"/journal/{day.year}/{day.month}/{day.day}/"
                })

            context.update({
                "week_start": week_start,
                "week_end": week_end,
                "prev_week": week_start - timedelta(days=7),
                "next_week": week_start + timedelta(days=7),
                "week_data": week_data,
            })

        return context


# =========================
# JournalOverView（表示専用）
# =========================
class JournalOverView(LoginRequiredMixin, View):
    template_name = 'journal/journal_over.html'

    def get(self, request, year, month, day):
        journal = Journal.objects.filter(
            user=request.user,
            date=date(year, month, day)
        ).first()

        # Journalが存在しない or 空なら Init に飛ばす
        if journal is None or (
            not journal.goals.exists() and
            not journal.todos.exists() and
            not journal.schedules.exists() and
            not journal.reflection.exists()
        ):
            return redirect('journal:journal_init', year=year, month=month, day=day)

        context = {
            "journal_date": journal.date,
            "goals": journal.goals.all(),
            "todos": journal.todos.all(),
            "schedules": journal.schedules.order_by("start_time"),
            "reflection": journal.reflection.first(),
            "prev_day": journal.date - timedelta(days=1),
            "next_day": journal.date + timedelta(days=1),
        }

        return render(request, self.template_name, context)


# =========================
# JournalInitView（作成専用）
# =========================
class JournalInitView(LoginRequiredMixin, View):
    template_name = 'journal/journal_init.html'
    login_url = 'accounts:login'

    def get(self, request, year, month, day):
        journal_date = date(year, month, day)

        # Journal を取得 or 作成
        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=journal_date
        )

        # フォームセットを初期化
        goal_formset = GoalFormSet(
            queryset=journal.goals.none(),   # まだ保存されていないので none
            prefix="goal",
            initial=[{}]  # extra フォームを確実に出す
        )

        todo_formset = TodoFormSet(
            queryset=journal.todos.none(),
            prefix="todo",
            initial=[{}]
        )

        context = {
            "journal": journal,
            "goal_formset": goal_formset,
            "todo_formset": todo_formset,
            "prev_day": journal_date - timedelta(days=1),
            "next_day": journal_date + timedelta(days=1),
            "journal_date": journal_date,
        }
        return render(request, self.template_name, context)

    def post(self, request, year, month, day):
        journal_date = date(year, month, day)
        journal = get_object_or_404(Journal, user=request.user, date=journal_date)

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
            # Goal 保存
            for goal in goal_formset.save(commit=False):
                if goal.title:
                    goal.journal = journal
                    goal.save()
            # Todo 保存
            for todo in todo_formset.save(commit=False):
                if todo.title:
                    todo.journal = journal
                    todo.save()

            return redirect(
                "journal:journal_over",
                year=year,
                month=month,
                day=day
            )

        # バリデーションエラーの場合は再表示
        context = {
            "journal": journal,
            "goal_formset": goal_formset,
            "todo_formset": todo_formset,
            "prev_day": journal_date - timedelta(days=1),
            "next_day": journal_date + timedelta(days=1),
            "journal_date": journal_date,
        }
        return render(request, self.template_name, context)

# =========================
# JournalDateRouterView（唯一の分岐）
# =========================
class JournalDateRouterView(LoginRequiredMixin, View):
    def get(self, request, year, month, day):
        target_date = date(year, month, day)
        has_journal_content = (
            Goal.objects.filter(journal__date=target_date, journal__user=request.user).exists()
            or Todo.objects.filter(journal__date=target_date, journal__user=request.user).exists()
            or Schedule.objects.filter(journal__date=target_date, journal__user=request.user).exists()
            or Reflection.objects.filter(journal__date=target_date, journal__user=request.user).exists()
        )

        if has_journal_content:
            return redirect(
                "journal:journal_over",
                year=year,
                month=month,
                day=day,
            )
        return redirect(
            "journal:journal_init",
            year=year,
            month=month,
            day=day,
        )