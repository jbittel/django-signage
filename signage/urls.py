from django.conf.urls import patterns
from django.conf.urls import url

from .views import DisplayView
from .views import DisplayJSONView


urlpatterns = patterns('',
    url(r'^(?P<pk>[\d]+)/$',
        DisplayView.as_view(), name='signage_display'),
    url(r'^(?P<display>[\d]+)/json/$',
        DisplayJSONView.as_view(), name='signage_display_json'),
)
