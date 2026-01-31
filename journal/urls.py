from django.urls import path
from journal.views.home_journal import HomeScreenView, JournalInitView, JournalOverView, JournalDateRouterView
from journal.views.goal import UpdateGoalView, DeleteGoalView, CreateGoalView 
from journal.views.todo import UpdateTodoView, DeleteTodoView, CreateTodoView, TodoToggleView
from journal.views.schedule import UpdateScheduleView, DeleteScheduleView, CreateScheduleView
from journal.views.reflection import CreateReflectionView, UpdateReflectionView

app_name = 'journal'

urlpatterns = [
    # ホーム画面
    path('', HomeScreenView.as_view(), name='home'),

    # 日付ルータ（Homeからリンクされる）
    path('journal/<int:year>/<int:month>/<int:day>/', JournalDateRouterView.as_view(), name='journal_router'),

    # JournalOver / JournalInit
    path('journal/<int:year>/<int:month>/<int:day>/over/', JournalOverView.as_view(), name='journal_over'),
    path('journal/<int:year>/<int:month>/<int:day>/init/', JournalInitView.as_view(), name='journal_init'),

    # Todo
    path('journal/<int:year>/<int:month>/<int:day>/todo/create/', CreateTodoView.as_view(), name='create_todo'),
    path('journal/todo/update/<int:pk>/', UpdateTodoView.as_view(), name='update_todo'),
    path('journal/todo/delete/<int:pk>/', DeleteTodoView.as_view(), name='delete_todo'),
    path('journal/todo/toggle/<int:pk>/', TodoToggleView.as_view(), name='toggle_todo'),

    # Goal
    path('journal/<int:year>/<int:month>/<int:day>/goal/create/', CreateGoalView.as_view(), name='create_goal'),
    path('journal/goal/update/<int:pk>/', UpdateGoalView.as_view(), name='update_goal'),
    path('journal/goal/delete/<int:pk>/', DeleteGoalView.as_view(), name='delete_goal'),

    # Schedule
    path('journal/<int:year>/<int:month>/<int:day>/schedule/create/', CreateScheduleView.as_view(), name='create_schedule'),
    path('journal/schedule/update/<int:pk>/', UpdateScheduleView.as_view(), name='update_schedule'),
    path('journal/schedule/delete/<int:pk>/', DeleteScheduleView.as_view(), name='delete_schedule'),

    # Reflection
    path('journal/<int:year>/<int:month>/<int:day>/reflection/create/', CreateReflectionView.as_view(), name='create_reflection'),
    path('journal/reflection/update/<int:pk>/', UpdateReflectionView.as_view(), name='update_reflection'),
]
