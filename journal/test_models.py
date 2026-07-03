import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from journal.models import Goal, Journal, Reflection, Schedule, Todo

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def journal(user):
    return Journal.objects.create(user=user, date="2026-07-01")


@pytest.mark.django_db
class TestJournal:
    def test_str(self, journal):
        assert str(journal) == "testuser - 2026-07-01"

    def test_unique_per_user_and_date(self, user, journal):
        with pytest.raises(IntegrityError):
            Journal.objects.create(user=user, date="2026-07-01")


@pytest.mark.django_db
class TestGoal:
    def test_str_and_relation(self, journal):
        goal = Goal.objects.create(title="散歩する", journal=journal)

        assert str(goal) == "散歩する"
        assert goal in journal.goals.all()


@pytest.mark.django_db
class TestTodo:
    def test_default_is_done_false(self, journal):
        todo = Todo.objects.create(title="買い物", journal=journal)

        assert todo.is_done is False
        assert todo in journal.todos.all()


@pytest.mark.django_db
class TestSchedule:
    def test_ordering_by_start_time(self, journal):
        Schedule.objects.create(
            journal=journal, title="夜の予定", start_time="20:00", end_time="21:00"
        )
        Schedule.objects.create(
            journal=journal, title="朝の予定", start_time="08:00", end_time="09:00"
        )

        titles = list(journal.schedules.values_list("title", flat=True))

        assert titles == ["朝の予定", "夜の予定"]


@pytest.mark.django_db
class TestReflection:
    def test_str(self, journal):
        reflection = Reflection.objects.create(journal=journal, content="良い一日だった")

        assert str(reflection) == "2026-07-01の振り返り"
