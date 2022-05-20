from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import Event, group_events_by_year, Tag
from urllib.parse import unquote, urlencode


def info(request):
    print(request.POST)
    try:
        from_year, to_year, tags = request.POST["from"], request.POST["to"], request.POST["tags"]
        print(tags)
        tags = tags.split(",")
        if tags[0] == "":
            tags.pop(0)
        print(tags)
    except:
        redirect("/app/")

    try:
        events = Event.objects.filter(date__range=["%s-01-01" % from_year, "%s-01-01" % to_year]).order_by('date')
        for t in tags:
            events = events.filter(tags__contains=t)
        grouped_events = group_events_by_year(events)
    except Exception as e:
        print(e)
        grouped_events = [[{"title": "Error"}]]
    # return render(request, 'app/index.html', {"text": "Welcome", "events": events})
    return render(request, 'app/info.html', {"grouped_events": grouped_events})

def index(request, name):
    print(name)
    showtags = False
    tags = []
    try:
        showtags = bool(request.GET["showtags"])
        tags = Tag.objects.all().order_by("name")
        if request.GET["filter"] is not None:
            tags = tags.filter(name__icontains=request.GET["filter"])
        if request.GET["newtag"] is not None:
            redirect("/app?showtags=true")
    except Exception as e:
        print(e)


    url = urlencode(dict(request.GET))
    print(unquote(url))
    return render(request, 'app/index.html', {"name": name, "showtags": showtags, "tags": tags})

def tags(request):
    print(request.GET["tags"])
    return render(request, 'app/index.html', {})
