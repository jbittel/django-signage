from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import Display
from .models import Slide


class DisplayDetail(DetailView):
    model = Display


class DisplayList(ListView):
    model = Display


class DisplayUpdate(UpdateView):
    model = Display
    fields = ['name', 'description', 'tags']


class SlideList(ListView):
    model = Slide


class SlideUpdate(UpdateView):
    model = Slide
    fields = ['name', 'description', 'image', 'start', 'end', 'duration', 'weight', 'tags']
