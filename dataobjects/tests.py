from django.test import TestCase
from dataobjects.models import Dataset
from django.db import IntegrityError

# Create your tests here.


class DatasetTestCase(TestCase):
    def test_create_dataset_default_description(self):
        dataset = Dataset(title='Test Dataset')
        dataset.save()
        self.assertEqual(len(Dataset.objects.all()), 1)
        created_dataset = Dataset.objects.first()
        self.assertEqual(created_dataset.title, 'Test Dataset')
        self.assertEqual(created_dataset.description,
                         Dataset.DEFAULT_DATASET_DESCRIPTION)
        self.assertEqual(created_dataset.name, 'test-dataset')

    def test_create_dataset(self):
        dataset = Dataset(title='Test Dataset',
                          description='This is a dataset description')
        dataset.save()
        self.assertEqual(len(Dataset.objects.all()), 1)
        created_dataset = Dataset.objects.first()
        self.assertEqual(created_dataset.title, 'Test Dataset')
        self.assertEqual(created_dataset.description,
                         'This is a dataset description')
        self.assertEqual(created_dataset.name, 'test-dataset')

    def test_modify_dataset(self):
        dataset = Dataset(title='Test Dataset')
        dataset.save()
        self.assertEqual(len(Dataset.objects.all()), 1)
        self.assertEqual(Dataset.objects.first().title, 'Test Dataset')
        self.assertEqual(Dataset.objects.first().name, 'test-dataset')
        self.assertEqual(Dataset.objects.first().description,
                         Dataset.DEFAULT_DATASET_DESCRIPTION)

        dataset.title = 'Modified Test Dataset'
        dataset.description = 'This is a dataset description'
        dataset.save()
        self.assertEqual(len(Dataset.objects.all()), 1)
        self.assertEqual(Dataset.objects.first().title,
                         'Modified Test Dataset')
        self.assertEqual(Dataset.objects.first().name, 'test-dataset')
        self.assertEqual(Dataset.objects.first().description,
                         'This is a dataset description')
        self.assertGreater(Dataset.objects.first().modification_date,
                           Dataset.objects.first().creation_date)

    def test_delete_dataset(self):
        dataset = Dataset(title='Test Dataset')
        dataset.save()
        self.assertEqual(len(Dataset.objects.all()), 1)
        dataset.delete()
        self.assertEqual(len(Dataset.objects.all()), 0)

    def test_name_is_unique(self):
        Dataset.objects.create(title='Test Dataset')
        with self.assertRaises(IntegrityError):
            Dataset.objects.create(title='Test Dataset')
