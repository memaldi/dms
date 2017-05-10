from dataobjects.models import Dataset, Resource
from rest_framework import serializers


class DatasetSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    resources = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='resources')

    class Meta:
        model = Dataset
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    dataset = serializers.HyperlinkedRelatedField(
        queryset=Dataset.objects.all(), view_name='dataset_detail')

    class Meta:
        model = Resource
        fields = '__all__'
