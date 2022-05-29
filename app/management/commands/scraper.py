import re
import requests
import shelve
import queue
import datetime
from app.models import Event, Tag
from django.core.management.base import BaseCommand, CommandError
import unicodedata

class Command(BaseCommand):
    help = 'Scrape for events'
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        pass

    pass

store = shelve.open("store")
queries = [
    (r">Date<\/th><td.*?>(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})", 3, [3, 2, 1]),
    (r">Date<\/th><td.*?>(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December)\s?(?:-|–)\s?(?:January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})", 3,  [3, 2, 1]),
    (r">Date<\/th><td.*?>(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})\s?(?:-|–)\s?(?:\d{1,2}) (?:January|February|March|April|May|June|July|August|September|October|November|December) (?:\d{1,4})", 3, [3, 2, 1]),
    (r">Date<\/th><td.*?>(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December)\s?(?:-|–)\s?(?:\d{1,2}) (?:January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})", 3,  [3, 2, 1]),
    (r">Date<\/th><td.*?>(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})\s?(?:-|–)\s?(?:January|February|March|April|May|June|July|August|September|October|November|December) (?:\d{1,4})", 2, [2, 1]),
    (r">Date<\/th><td.*?>(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}),? (\d{1,4})", 3, [2, 3, 1]),
    (r">Date<\/th><td.*?>(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})\s?(?:-|–)\s?(?:January|February|March|April|May|June|July|August|September|October|November|December) (?:\d{1,2}),\s?(\d{1,4})", 3, [2, 3, 1]),
    (r">Date<\/th><td.*?>(\d{1,2}) ?(?:-|–) ?\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,4})", 3, [3, 2, 1]),
    (r">Date<\/th><td.*?>(\d{1,4}) ?(?:-|–) ?(?:\d{1,4})", 1, [1]),
    (r">Date<\/th><td.*?>(\d{1,4})", 1, [1]),
]

MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}
def get_event_date(page: str) -> str:
    for q in queries:
        query, n, order = q

        m = re.search(query, page)
        out = [0, 1, 1]
        try:
            for i in range(n):
                v = m.group(i+1)
                if v in MONTHS.keys():
                    out[order[i]-1] = MONTHS[v]
                else:
                    out[order[i]-1] = int(v)
            break
        except Exception as e:
            out = [0, 1, 1]
            pass
    if out[0] == 0:
        return None
    return out + [1] * (3-len(out))

def get_tags(page: str):
    page = page[page.find(">Categories</a>:"):page.find("This page was last edited")]
    query = "(?:(?:>)([a-zA-Z\s0-9]+?)(?:</a>))+"
    m = re.findall(query, page)
    if len(m) == 0:
        return []
    m.pop(0)
    tags = []
    for match in m:
        tags.append(match)
    return tags

def test_website(l: str):
    response = requests.get("https://en.wikipedia.org%s" % l)
    # data = response.content.decode('utf-8').replace("&#160;", " ").replace("–".encode('utf-8'), "-")
    data = response.content.decode('utf-8')
    data = data.replace("&#160;", " ")
    # data = data.replace(b'\xe2\x80\x94'.decode('utf-8'), '-')
    date = get_event_date(data)
    print(date)

    d = 0
    if date is not None:
        try:
            d = datetime.datetime(date[0], date[1], date[2])
        except ValueError:
            d = datetime.datetime(day=date[0], month=date[1], year=date[2])
            pass
        # Event.objects.create(title=l, date=d, link=l)
    print(l, d)

def get_links(page: str) -> list:
    links = re.findall(r"(?:<a *.? href=\"(\/wiki.*?)\")", page)
    return links

start = '/wiki/Mexican_Dirty_War'
links = []
wrong_prefixes = ["/wiki/Wikipedia", "/wiki/Category", "wiki/Main_Page", "/wiki/Special", "/wiki/File", "/wiki/Help", "/wiki/SVG", "/wiki/Template"]
queue = queue.Queue()
# queue.put(start)

TAGS = {}
def init_tags():
    tags = Tag.objects.all()
    for tag in tags:
        TAGS[tag.name] = tag.id

def scrape():
    while not queue.empty():
        l = queue.get()
        print(l)

        if l in store and not queue.empty():
            continue
        store[l] = True

        stop = False
        for prefix in wrong_prefixes:
            if prefix in l:
                stop = True
        if stop:
            continue
        response = requests.get("https://en.wikipedia.org%s" % l)
        data = response.content.decode('utf-8')
        data = data.replace("&#160;", " ")

        date = get_event_date(data)
        tags = get_tags(data)
        if date is not None:
            try:
                d = datetime.datetime(date[0], date[1], date[2])
            except ValueError:
                d = datetime.datetime(day=date[0], month=date[1], year=date[2])
                pass
            title =l[6:].replace("_", " ")
            tags_str = ",".join(tags)
            event = Event.objects.create(title=title, date=d, link="https://en.wikipedia.org"+l, tags=tags_str)
            print(l, d)

            for t in tags:
                try:
                    tag = Tag.objects.get(name=t)
                except Tag.DoesNotExist:
                    tag = Tag.objects.create(name=t)

        new_links = get_links(data)
        for link in new_links:
            queue.put(link)
try:
    try:
        f = open("queue", "x")
    except:
        pass

    f = open("queue").read()
    for item in f.split(",,,"):
        item = item.strip("\n")
        queue.put(item)
    scrape()

except KeyboardInterrupt:
    list = ""
    f = open("queue", "w")
    while not queue.empty():
        list += queue.get() + ",,,"
    f.write(list)
    f.close()
    exit()
    # test_website("//wiki/Maquis_du_Mont_Mouchet")
