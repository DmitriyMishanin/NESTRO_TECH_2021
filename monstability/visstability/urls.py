from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('diagram/', views.diagram, name='diagram'),
    path('model/', views.model, name='model'),
    path('tablestead/', views.tablestead, name='tablestead'),
    path('tableedge/', views.tableedge, name='tableedge'),
    path('about/', views.about, name='about'),
]
