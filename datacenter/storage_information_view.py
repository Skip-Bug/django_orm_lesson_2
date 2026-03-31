from datacenter.models import Visit, Passcard
from datacenter.models import format_duration, is_visit_long
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at__isnull=True)

    for visit in visits:
        duration, entered, is_long = is_visit_long(visit, minutes=60)
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': entered,
                'duration': format_duration(duration),
                'is_strange': is_long,
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
