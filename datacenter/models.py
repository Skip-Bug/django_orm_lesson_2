from django.db import models
from datetime import timedelta
from django.utils.timezone import localtime


SECONDS_PER_MINUTE = 60
"""Количество секунд в одной минуте."""

MINUTES_PER_HOUR = 60
"""Количество минут в одном часе."""

SECONDS_PER_HOUR = SECONDS_PER_MINUTE * MINUTES_PER_HOUR
"""Количество секунд в одном часе (60 × 60 = 3600)."""

DEFAULT_LONG_VISIT = 60
"""Длительность визита для подозрения в минутах."""


def format_duration(duration):
    """Форматирует timedelta в строку Ч:М:С."""
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // SECONDS_PER_HOUR
    minutes = (total_seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
    seconds = total_seconds % SECONDS_PER_MINUTE
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def get_duration(visit):
    """Получает длительность (в секундах)."""
    entered = localtime(visit.entered_at)
    if visit.leaved_at is None:
        now = localtime()
        duration = now - entered
    else:
        leaved = localtime(visit.leaved_at)
        duration = leaved - entered
    return duration


def is_visit_long(visit, minutes=DEFAULT_LONG_VISIT):
    """Проверяет подозрительную длительность."""
    duration = get_duration(visit)
    is_long = duration > timedelta(minutes=minutes)
    return is_long


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
