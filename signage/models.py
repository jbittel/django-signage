from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeFramedModel
from sortedm2m.fields import SortedManyToManyField


@python_2_unicode_compatible
class Slide(models.Model):
    """
    """
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='slides/')
    duration = models.PositiveIntegerField(_('duration'), default=7)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Slider(models.Model):
    """
    """
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    slides = SortedManyToManyField(Slide)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Video(TimeFramedModel):
    """
    """
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('video url'))

    def __str__(self):
        return self.title

    @property
    def duration(self):
        return self.end - self.start


@python_2_unicode_compatible
class Display(models.Model):
    """
    """
    name = models.CharField(_('name'), max_length=255)
    location = models.CharField(_('location'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    slider = models.ForeignKey(Slider, on_delete=models.PROTECT)
    video = models.ManyToManyField(Video, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signage_display', args=[str(self.pk)])

    def get_json_url(self):
        return self.get_absolute_url() + 'json/'
