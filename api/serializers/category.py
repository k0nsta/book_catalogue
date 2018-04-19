from rest_framework import serializers

from catalogue.models import Category


class CategorySerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='title')
    create = serializers.CharField(source='create_date')

    class Meta:
        model = Category
        fields = ('id', 'category', 'create')
