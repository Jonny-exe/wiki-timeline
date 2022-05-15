from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import Event, Tag, EventTag, group_events_by_year
from urllib.parse import unquote, urlencode




def info(request):
    print(request.POST)
    try:
        from_year, to_year, tags = request.POST["from"], request.POST["to"], request.POST["tags"]
        tags = tags.split(",")
        print(tags)
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
    showtags = False
    tags = []
    try:
        showtags = bool(request.GET["showtags"])
        tags = Tag.objects.all()
        if request.GET["filter"] is not None:
            tags = tags.filter(name__icontains=request.GET["filter"])
        if request.GET["newtag"] is not None:
            del request.GET["newtag"]
    except Exception as e:
        print(e)

    redirect("/app/")

    url = urlencode(dict(request.GET))
    print(unquote(url))
    return render(request, 'app/index.html', {"url": url, "showtags": showtags, "tags": tags})

def tags(request):
    print(request.GET["tags"])
    return render(request, 'app/index.html', {})
