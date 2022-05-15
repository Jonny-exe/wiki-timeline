from django.db import models
from urllib.parse import unquote
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    link = models.CharField(max_length=400)
    # tags = models.ArrayField(models.ForeignKey(Tag, on_delete=models.CASCADE))

class Tag(models.Model):
    name = models.CharField(max_length=30)

class EventTag(models.Model):
    event_id = models.IntegerField()
    tag_id = models.IntegerField()

def group_events_by_year(events: []):
    grouped_events = [[]]
    group_idx = 0;
    if len(events) == 0:
        return []

    current_year = events[0].date.year
    for event in events:
        event.title = unquote(event.title)
        if event.date.year == current_year:
            grouped_events[group_idx].append(event)
        else:
            grouped_events.append([event])
            current_year = event.date.year
            group_idx += 1
    return grouped_events
