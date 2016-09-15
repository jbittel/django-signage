from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
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


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DisplayDetail(DetailView):
    model = Display


class DisplayList(StaffRequiredMixin, ListView):
    model = Display


class DisplayCreate(StaffRequiredMixin, CreateView):
    model = Display
    fields = ['name', 'update_interval', 'tags']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(DisplayCreate, self).form_valid(form)


class DisplayDelete(StaffRequiredMixin, DeleteView):
    model = Display
    success_url = reverse_lazy('signage:display_list')


class DisplaySlides(ListAPIView):
    serializer_class = SlideSerializer

    def get_queryset(self):
        display = get_object_or_404(Display, pk=self.kwargs['pk'])
        return display.get_slides()


class DisplayVideo(RetrieveAPIView):
    serializer_class = VideoSerializer

    def get_object(self):
        display = get_object_or_404(Display, pk=self.kwargs['pk'])
        return display.get_video()


class DisplayUpdate(StaffRequiredMixin, UpdateView):
    model = Display
    fields = ['name', 'update_interval', 'tags']


class SlideList(StaffRequiredMixin, ListView):
    model = Slide


class SlideCreate(StaffRequiredMixin, CreateView):
    model = Slide
    fields = ['name', 'image', 'start', 'end', 'duration', 'weight', 'tags']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(SlideCreate, self).form_valid(form)


class SlideDelete(StaffRequiredMixin, DeleteView):
    model = Slide
    success_url = reverse_lazy('signage:slide_list')


class SlideUpdate(StaffRequiredMixin, UpdateView):
    model = Slide
    fields = ['name', 'image', 'start', 'end', 'duration', 'weight', 'tags']


class VideoList(StaffRequiredMixin, ListView):
    model = Video


class VideoCreate(StaffRequiredMixin, CreateView):
    model = Video
    fields = ['name', 'url', 'start', 'end', 'tags']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(VideoCreate, self).form_valid(form)


class VideoDelete(StaffRequiredMixin, DeleteView):
    model = Video
    success_url = reverse_lazy('signage:video_list')


class VideoUpdate(StaffRequiredMixin, UpdateView):
    model = Video
    fields = ['name', 'url', 'start', 'end', 'tags']
