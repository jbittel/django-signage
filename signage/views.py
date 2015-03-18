from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from django.views.generic import View
from django.views.generic import DetailView

from .models import Display
from .models import Slider
from .models import Video
from .serializer import serialize


class DisplayView(DetailView):
    model = Display
    context_object_name = 'display'


class DisplayJSONView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseNotAllowed(['XMLHttpRequest'])
        return super(DisplayJSONView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        objects = self.get_object_data(**kwargs)
        return self.render_json_response(objects)

    def get_object_data(self, **kwargs):
        display = {'display__pk': kwargs['display']}
        if Video.timeframed.filter(**display).count():
            return Video.timeframed.filter(**display)
        else:
            return Slider.objects.get(**display).slides.all()

    def render_json_response(self, objects):
        return HttpResponse(serialize(objects), content_type='application/json')
