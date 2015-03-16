from django.contrib import admin

from .models import Display
from .models import Slide
from .models import Slider
from .models import Video


admin.site.register(Display)
admin.site.register(Slide)
admin.site.register(Slider)
admin.site.register(Video)
