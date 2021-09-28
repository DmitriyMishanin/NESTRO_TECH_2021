from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import viewsapi

URL_FORMAT_OVERRIDE = 'params'

urlpatterns = format_suffix_patterns([
    path('nodes/', viewsapi.NodesViewSet.as_view({'get': 'list', 'post': 'create',})),
    path('nodes/<str:id_gr>/', viewsapi.NodesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy',})),
    path('edges/', viewsapi.EdgesViewSet.as_view({'get': 'list', 'post': 'create',})),
    path('edges/<str:id_gr>', viewsapi.EdgesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy',})),
    path("nodesview/", viewsapi.NodesListView.as_view()),
    path("steptest/", viewsapi.steptest),
])
