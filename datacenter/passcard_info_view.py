from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
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
    entered = localtime(visit.entered_at)
    if visit.leaved_at is None:
        now = localtime()
        duration = now - entered
    else:
        leaved = localtime(visit.leaved_at)
        duration = leaved - entered
    return duration, entered


def is_visit_long(visit, minutes=60):
    duration, entered = get_duration(visit)
    is_long = duration > timedelta(minutes=minutes)
    return duration, entered, is_long


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    # Программируем здесь
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    print(visits)
    for visit in visits:
        duration, entered, is_long = is_visit_long(visit, minutes=60)

        this_passcard_visits.append({
            'entered_at': entered,
            'duration': format_duration(duration),
            'is_strange': is_long,
        })
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
