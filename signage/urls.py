from django.conf.urls import url

from .views import DisplayCreate
from .views import DisplayDetail
from .views import DisplayList
from .views import DisplayUpdate
from .views import SlideCreate
from .views import SlideList
from .views import SlideUpdate


app_name = 'signage'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', DisplayDetail.as_view(), name='display'),
    url(r'^displays/$', DisplayList.as_view(), name='display_list'),
    url(r'^displays/create/$', DisplayCreate.as_view(), name='display_create'),
    url(r'^displays/update/(?P<pk>\d+)/$', DisplayUpdate.as_view(), name='display_update'),
    url(r'^slides/$', SlideList.as_view(), name='slide_list'),
    url(r'^slides/create/$', SlideCreate.as_view(), name='slide_create'),
    url(r'^slides/update/(?P<pk>\d+)/$', SlideUpdate.as_view(), name='slide_update'),
]
