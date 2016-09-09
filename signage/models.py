from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from model_utils.models import TimeFramedModel
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Content(TimeFramedModel):
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )

    tags = TaggableManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def active(self):
        return (self.start is None or self.start <= now()) and (self.end is None or self.end >= now())

    def get_absolute_url(self):
        return reverse("signage:%s_update" % self._meta.verbose_name, args=[self.pk])

    def get_displays(self):
        return Display.objects.filter(tags__name__in=self.tags.names()).distinct()


class Slide(Content):
    image = models.ImageField(
        upload_to='slides/',
    )
    duration = models.PositiveIntegerField(
        default=7,
    )
    weight = models.SmallIntegerField(
        default=0,
    )


class Video(Content):
    url = models.URLField()


@python_2_unicode_compatible
class Display(models.Model):
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
        return Slide.timeframed.filter(tags__name__in=self.tags.names()).order_by('weight').distinct()

    def get_video(self):
        return Video.timeframed.filter(tags__name__in=self.tags.names()).distinct().first()
