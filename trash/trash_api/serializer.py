from rest_framework import serializers
from django.conf import settings

class StaticImageSerializer(serializers.Serializer):
    image_name = serializers.CharField()

    def get_image_url(self, obj):
        return f"{settings.STATIC_URL}/{obj}"