import hashlib
import json

from django.core.serializers.json import Serializer
from django.template.loaders.app_directories import Loader
from django.utils.encoding import smart_text


class FlatSerializer(Serializer):
    def get_dump_object(self, obj):
        self._current['type'] = smart_text(obj._meta).split('.')[1]
        return self._current

    def get_template_hash(self, template_name):
        loader = Loader()
        source, origin = loader.load_template_source(template_name)
        return hashlib.sha1(source).hexdigest()

    def getvalue(self):
        objects = super(FlatSerializer, self).getvalue()
        data = {
            'hash': self.get_template_hash('signage/display_detail.html'),
            'slides': json.loads(objects),
        }
        return json.dumps(data)


def serialize(queryset):
    model_name = queryset.model.__name__
    if model_name == 'Slide':
        fields = ('duration', 'image')
    elif model_name == 'Video':
        fields = ('url',)

    s = FlatSerializer()
    s.serialize(queryset, fields=fields)
    return s.getvalue()
