from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import Event, group_events_by_year

# Create your views here.
def index(request):
    try:
        # events = Event.objects.all()
        events = Event.objects.order_by('date')
        print(events, len(events), type(events))
        grouped_events = group_events_by_year(events)
    except Exception as e:
        print(e)
        grouped_events = [[{"title": "Error"}]]
    print(grouped_events)
    # return render(request, 'app/index.html', {"text": "Welcome", "events": events})
    return render(request, 'app/index.html', {"text": "Welcome", "grouped_events": grouped_events})
