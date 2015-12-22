from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeFramedModel
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Slide(TimeFramedModel):
    """
    """
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )
    image = models.ImageField(
        upload_to='slides/',
    )
    duration = models.PositiveIntegerField(
        default=7,
    )
    weight = models.SmallIntegerField(
        default=0,
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signage:slide_update', args=[self.pk])

    def get_displays(self):
        return Display.objects.filter(tags__name__in=self.tags.names()).distinct()


@python_2_unicode_compatible
class Display(models.Model):
    """
    """
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signage:display_update', args=[self.pk])

    def get_slides(self):
        return Slide.objects.filter(tags__name__in=self.tags.names()).distinct()
