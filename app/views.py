from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import Event, group_events_by_year

def info(request):
    print(request.POST)
    try:
        from_year, to_year, tags = request.POST["from"], request.POST["to"], request.POST["tags"]
        tags = tags.split(",")
    except:
        redirect("/app/")

    try:
        # events = Event.objects.all()
        events = Event.objects.filter(date__range=["%s-01-01" % from_year, "%s-01-01" % to_year]).order_by('date')
        grouped_events = group_events_by_year(events)
    except Exception as e:
        print(e)
        grouped_events = [[{"title": "Error"}]]
    # return render(request, 'app/index.html', {"text": "Welcome", "events": events})
    return render(request, 'app/info.html', {"grouped_events": grouped_events})

def index(request):
    return render(request, 'app/index.html', {})
