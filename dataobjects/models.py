from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.urls import reverse

# Create your models here.


class Dataset(models.Model):
    DEFAULT_DATASET_DESCRIPTION = _('No description is provided for this '
                                    'dataset')

    title = models.CharField(max_length=50)
    name = models.SlugField(max_length=50, unique=True)
    description = models.TextField(
        default=DEFAULT_DATASET_DESCRIPTION)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = slugify(self.title)
        super(Dataset, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dataset_detail', args=[str(self.id)])


class Resource(models.Model):
    DEFAULT_RESOURCE_DESCRIPTION = _('No description is provided for this '
                                     'resource')

    title = models.CharField(max_length=50)
    description = models.TextField(
        default=DEFAULT_RESOURCE_DESCRIPTION)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    _format = models.CharField(max_length=10)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
