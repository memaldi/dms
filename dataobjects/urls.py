from django.conf.urls import url
from dataobjects import views

urlpatterns = [
    url(r'^dataset/$', views.DatasetList.as_view(), name='dataset'),
    url(r'^dataset/new/$', views.new_dataset, name='dataset_new'),
    url(r'^dataset/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view(),
        name='dataset_detail'),
    url(r'^dataset/(?P<pk>[0-9]+)/edit/$', views.edit_dataset,
        name='dataset_edit'),
    url(r'^dataset/(?P<pk>[0-9]+)/delete/$', views.delete_dataset,
        name='dataset_delete'),
    url(r'^dataset/(?P<dataset_pk>[0-9]+)/resource/$',
        views.ResourceList.as_view(),
        name='resource'),
    url(r'^dataset/(?P<dataset_pk>[0-9]+)/resource/(?P<pk>[0-9]+)/$',
        views.ResourceDetail.as_view(),
        name='resource_detail'),
]
