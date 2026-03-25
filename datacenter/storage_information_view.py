from datacenter.models import Visit
from datacenter.models import Passcard
from django.shortcuts import render
from django.utils.timezone import localtime
import datetime


def format_duration(duration):
    """Форматирует timedelta в строку Ч:М:С."""
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def get_duration(visit):
    now = localtime()
    moscow_entered = localtime(visit.entered_at)
    duration = now - moscow_entered
    return duration, moscow_entered


def storage_information_view(request):
    # Программируем здесь
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at__isnull=True)

    for visit in visits:
        duration, moscow_entered = get_duration(visit)
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': moscow_entered,
                'duration': format_duration(duration),
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
