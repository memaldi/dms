from django.test import TestCase, Client
from dataobjects.models import Dataset, Resource
from dataobjects.forms import DatasetForm
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from unittest import skip
import json
import base64

# Create your tests here.

BASIC_USER = 'test-user'
BASIC_PASSWORD = 'test-password'


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


class ResourceTestCase(TestCase):
    def test_create_resource_default_description(self):
        dataset = Dataset(title='Test dataset')
        dataset.save()
        resource = Resource(title='Test resource', _format='CSV',
                            dataset=dataset)
        resource.save()
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(Resource.objects.first().title, 'Test resource')
        self.assertEqual(Resource.objects.first().description,
                         Resource.DEFAULT_RESOURCE_DESCRIPTION)
        self.assertEqual(Resource.objects.first()._format, 'CSV')
        self.assertEqual(Resource.objects.first().dataset, dataset)

    def test_create_resource(self):
        dataset = Dataset(title='Test dataset')
        dataset.save()
        resource = Resource(title='Test resource', _format='CSV',
                            description='This is a resource description',
                            dataset=dataset)
        resource.save()
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(Resource.objects.first().title, 'Test resource')
        self.assertEqual(Resource.objects.first().description,
                         'This is a resource description')
        self.assertEqual(Resource.objects.first()._format, 'CSV')
        self.assertEqual(Resource.objects.first().dataset, dataset)

    def test_modify_resource(self):
        dataset = Dataset(title='Test dataset')
        dataset.save()
        resource = Resource(title='Test resource', _format='CSV',
                            dataset=dataset)
        resource.save()
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(Resource.objects.first().title, 'Test resource')
        self.assertEqual(Resource.objects.first()._format, 'CSV')
        resource.title = 'Modified Test Resource'
        resource._format = 'JSON'
        resource.save()
        self.assertEqual(Resource.objects.first().title,
                         'Modified Test Resource')
        self.assertEqual(Resource.objects.first()._format, 'JSON')

    def _delete_dataset_and_resource(self, on_cascade=False):
        dataset = Dataset(title='Test dataset')
        dataset.save()
        resource = Resource(title='Test resource', _format='CSV',
                            dataset=dataset)
        resource.save()
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(len(Dataset.objects.all()), 1)
        if on_cascade:
            dataset.delete()
        else:
            resource.delete()
        if on_cascade:
            self.assertEqual(len(Dataset.objects.all()), 0)
        else:
            self.assertEqual(len(Dataset.objects.all()), 1)
        self.assertEqual(len(Resource.objects.all()), 0)

    def test_delete_resource(self):
        self._delete_dataset_and_resource()

    def test_delete_resource_on_cascade(self):
        self._delete_dataset_and_resource(on_cascade=True)


class DatasetFormTestCase(TestCase):
    def test_create_dataset_form(self):
        form = DatasetForm({
            'title': 'Test dataset',
            'name': 'test-dataset',
            'description': 'This is a test dataset.'
        })

        self.assertEqual(True, form.is_valid())

        dataset = form.save()

        self.assertEqual('Test dataset', dataset.title)
        self.assertEqual('test-dataset', dataset.name)
        self.assertEqual('This is a test dataset.', dataset.description)

    def test_create_dataset_invalid_name(self):
        form = DatasetForm({
            'title': 'Test dataset',
            'name': 'test-dataset',
            'description': 'This is a test dataset.'
        })

        self.assertEqual(True, form.is_valid())

        dataset = form.save()

        self.assertEqual('Test dataset', dataset.title)
        self.assertEqual('test-dataset', dataset.name)
        self.assertEqual('This is a test dataset.', dataset.description)

        form = DatasetForm({
            'title': 'Test dataset',
            'name': 'test-dataset',
            'description': 'This is a test dataset.'
        })

        self.assertEqual(False, form.is_valid())


class DatasetListJSONTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        dataset = Dataset(title='Dataset title',
                          description='Dataset description')
        dataset.save()

    def test_get_datasets_json(self):
        headers = {'HTTP_ACCEPT': 'application/json'}
        response = self.client.get('/dataset/', **headers)

        self.assertEqual(200, response.status_code)

        response_json = json.loads(response.content)

        self.assertEqual(1, len(response_json))
        self.assertEqual('Dataset title', response_json[0]['title'])
        self.assertEqual('Dataset description',
                         response_json[0]['description'])
        self.assertEqual('dataset-title', response_json[0]['name'])

    def test_post_dataset_json(self):
        self.assertEqual(1, Dataset.objects.count())

        headers = {'HTTP_ACCEPT': 'application/json',
                   'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                       base64.b64encode('{}:{}'.format(
                            BASIC_USER, BASIC_PASSWORD).encode()).decode())}
        body = {'title': 'Another dataset',
                'name': 'another-dataset',
                'description': 'Another dataset description'}
        response = self.client.post('/dataset/', json.dumps(body),
                                    content_type='application/json', **headers)

        self.assertEqual(201, response.status_code)

        self.assertEqual(2, Dataset.objects.count())


class DatasetListHTMLTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        dataset = Dataset(title='Dataset title',
                          description='Dataset description')
        dataset.save()

    def test_get_datasets_html(self):
        headers = {'HTTP_ACCEPT': 'text/html'}
        response = self.client.get('/dataset/', **headers)

        self.assertEqual(200, response.status_code)

        expected = render_to_string('dataobjects/datasets.html',
                                    {'datasets': Dataset.objects.all()})

        self.assertEqual(expected, response.content.decode())

    @skip
    def test_post_dataset_html(self):
        self.assertEqual(1, Dataset.objects.count())

        headers = {'HTTP_ACCEPT': 'application/json',
                   'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                       base64.b64encode('{}:{}'.format(
                            BASIC_USER, BASIC_PASSWORD).encode()).decode())}
        body = {'title': 'Another dataset',
                'name': 'another-dataset',
                'description': 'Another dataset description'}
        response = self.client.post('/dataset/', json.dumps(body),
                                    content_type='text/html', **headers)

        print(response.content)
        self.assertEqual(201, response.status_code)

        self.assertEqual(2, Dataset.objects.count())
