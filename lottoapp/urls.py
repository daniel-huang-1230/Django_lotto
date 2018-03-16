
from . import views
from django.urls import path, include, re_path
from django.views.generic import ListView, DetailView
from lottoapp.models import Event



urlpatterns = [
     #path('', views.index, name='index'),
     path('create_event/', views.create_event, name='create_event'),
     re_path(r'^$', ListView.as_view(queryset=Event.objects.all().order_by("-deadline")[:10], template_name="lottoapp/event_list.html")),
     re_path(r'^(?P<pk>\d+)$', DetailView.as_view(model=Event, template_name='lottoapp/event.html'))
]