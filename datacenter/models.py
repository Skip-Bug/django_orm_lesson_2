from django.db import models
from datetime import timedelta
from django.utils.timezone import localtime


def format_duration(duration):
    """Форматирует timedelta в строку Ч:М:С."""
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def get_duration(visit):
    """Получает длительность (в секундах)"""
    entered = localtime(visit.entered_at)
    if visit.leaved_at is None:
        now = localtime()
        duration = now - entered
    else:
        leaved = localtime(visit.leaved_at)
        duration = leaved - entered
    return duration, entered


def is_visit_long(visit, minutes=60):
    """Проверяет длительность """
    duration, entered = get_duration(visit)
    is_long = duration > timedelta(minutes=minutes)
    return duration, entered, is_long


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
