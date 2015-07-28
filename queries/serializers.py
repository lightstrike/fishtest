from rest_framework import serializers

from .models import FishQuery


class FishQuerySerializer(serializers.HyperlinkedModelSerializer):
    alaska_fish_game_url = serializers.ReadOnlyField(source='akfg_url')

    class Meta:
        '''
        From http://www.django-rest-framework.org/api-guide/serializers/#modelserializer:
        By default, all the model fields on the class will be mapped
        to a corresponding serializer fields.
        '''
        model = FishQuery