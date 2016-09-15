from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from model_utils.models import TimeFramedModel
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Content(TimeFramedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    name = models.CharField(
        max_length=255,
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
        default=10,
        choices=[(i, i) for i in range(5, 65, 5)],
        help_text='Number of seconds the slide is displayed.',
    )
    weight = models.SmallIntegerField(
        default=0,
        choices=[(i, i) for i in range(-10, 11)],
        help_text='Relative ordering of slides. Higher values appear earlier in the list.',
    )


class Video(Content):
    url = models.URLField(
        verbose_name='Stream URL',
        help_text='Absolute path to video streaming URL.'
    )


@python_2_unicode_compatible
class Display(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    name = models.CharField(
        max_length=255,
    )
    update_interval = models.PositiveIntegerField(
        default=10,
        choices=[(i, i) for i in range(10, 70, 10)],
        help_text='Number of seconds between checks for content changes.',
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signage:display_update', args=[self.pk])

    def get_slides(self):
        return Slide.timeframed.filter(tags__name__in=self.tags.names()).order_by('-weight').distinct()

    def get_video(self):
        return Video.timeframed.filter(tags__name__in=self.tags.names()).distinct().first()
