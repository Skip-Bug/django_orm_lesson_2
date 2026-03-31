from datacenter.models import Passcard, Visit
from django.shortcuts import render, get_object_or_404
from datacenter.models import format_duration, get_duration, is_visit_long
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits:
        duration = get_duration(visit)
        entered = localtime(visit.entered_at)
        is_long = is_visit_long(visit, minutes=60)

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
