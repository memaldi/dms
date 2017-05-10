from dataobjects.models import Dataset
from rest_framework import serializers


class DatasetSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Dataset
        fields = '__all__'
