from django.forms import ModelForm
from dataobjects.models import Dataset


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'name', 'description']
