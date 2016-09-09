from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from .models import Display
from .models import Slide
from .models import Video
from .serializers import SlideSerializer
from .serializers import VideoSerializer


class DisplayDetail(DetailView):
    model = Display


class DisplayList(ListView):
    model = Display


class DisplayCreate(CreateView):
    model = Display
    fields = ['name', 'description', 'tags']


class DisplayDelete(DeleteView):
    model = Display
    success_url = reverse_lazy('signage:display_list')


class DisplaySlides(ListAPIView):
    serializer_class = SlideSerializer

    def get_queryset(self):
        try:
            return Display.objects.get(pk=self.kwargs['pk']).get_slides()
        except Display.DoesNotExist:
            raise Http404


class DisplayVideo(RetrieveAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        try:
            return Display.objects.get(pk=self.kwargs['pk']).get_video()
        except Display.DoesNotExist:
            raise Http404


class DisplayUpdate(UpdateView):
    model = Display
    fields = ['name', 'description', 'tags']


class SlideList(ListView):
    model = Slide


class SlideCreate(CreateView):
    model = Slide
    fields = ['name', 'description', 'image', 'start', 'end', 'duration', 'weight', 'tags']


class SlideDelete(DeleteView):
    model = Slide
    success_url = reverse_lazy('signage:slide_list')


class SlideUpdate(UpdateView):
    model = Slide
    fields = ['name', 'description', 'image', 'start', 'end', 'duration', 'weight', 'tags']


class VideoList(ListView):
    model = Video


class VideoCreate(CreateView):
    model = Video
    fields = ['name', 'description', 'url', 'start', 'end', 'tags']


class VideoDelete(DeleteView):
    model = Video
    success_url = reverse_lazy('signage:video_list')


class VideoUpdate(UpdateView):
    model = Video
    fields = ['name', 'description', 'url', 'start', 'end', 'tags']
