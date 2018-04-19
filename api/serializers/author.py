from rest_framework import serializers

from catalogue.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'full_name', )
