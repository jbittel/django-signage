from django.conf.urls import url

from .views import DisplayDetail
from .views import DisplayList
from .views import DisplayUpdate
from .views import SlideList
from .views import SlideUpdate


app_name = 'signage'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', DisplayDetail.as_view(), name='display'),
    url(r'^displays/$', DisplayList.as_view(), name='display_list'),
    url(r'^displays/(?P<pk>\d+)/$', DisplayUpdate.as_view(), name='display_update'),
    url(r'^slides/$', SlideList.as_view(), name='slide_list'),
    url(r'^slides/(?P<pk>\d+)/$', SlideUpdate.as_view(), name='slide_update'),
]
