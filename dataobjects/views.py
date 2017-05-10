from dataobjects.models import Dataset
from dataobjects.forms import DatasetForm
from dataobjects.serializers import DatasetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


@permission_classes((IsAuthenticatedOrReadOnly,))
class DatasetList(APIView):
    def get(self, request, format=None):
        queryset = Dataset.objects.all()
        if request.accepted_renderer.format == 'html':
            context = {'datasets': queryset}
            return Response(context, template_name='dataobjects/datasets.html')
        serializer = DatasetSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticatedOrReadOnly,))
class DatasetDetail(APIView):
    def get(self, request, pk, format=None):
        dataset = get_object_or_404(Dataset, pk=pk)
        if request.accepted_renderer.format == 'html':
            context = {'dataset': dataset}
            return Response(context, template_name='dataobjects/dataset.html')
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dataset = get_object_or_404(Dataset, pk=pk)
        serializer = DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = get_object_or_404(Dataset, pk=pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def new_dataset(request):
    form = DatasetForm()
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            dataset = form.save()
            return redirect('dataset_detail', pk=dataset.id)

    context = {'form': form}
    return render(request, 'dataobjects/edit_dataset.html', context)


def edit_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    form = DatasetForm(instance=dataset)
    if request.method == 'POST':
        form = DatasetForm(request.POST, instance=dataset)
        if form.is_valid():
            form.save()
            return redirect('dataset_detail', pk=pk)

    context = {'form': form, 'pk': pk}
    return render(request, 'dataobjects/edit_dataset.html', context)


def delete_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    dataset.delete()
    return redirect('dataset')
