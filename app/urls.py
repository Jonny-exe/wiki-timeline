from django.urls import path

from . import views

urlpatterns = [
    path('info', views.info, name='search'),
    path('', views.index, name='index', kwargs={"name": ""}),
    path('<str:name>', views.index, name='index'),
    path('tags', views.tags, name='tags'),
]
