from rest_framework import views, viewsets, authentication, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Nodes, Edges
from .serializers import NodesSerializer, EdgesSerializer, NodesViewSerializer, EdgesViewSerializer
from .grstead import steptest_model

##### Nodes #####
class NodesViewSet(viewsets.ModelViewSet):
    """Nodes"""

    #permission_classes = [ObjectPermissions, ]
    serializer_class = NodesSerializer
    queryset = Nodes.objects.order_by('id')
    lookup_field = 'id_gr'


##### Edges #####
class EdgesViewSet(viewsets.ModelViewSet):
    """Edges"""

    #permission_classes = [ObjectPermissions, ]
    serializer_class = EdgesSerializer
    queryset = Edges.objects.order_by('id')
    lookup_field = 'id_gr'

##### Nodes and Edges #####
class NodesListView(views.APIView):
    """Nodes and Edges"""

    def get(self, request, format=None, **kwargs):
        nodeslst = Nodes.objects.all()
        nodes_serializer = NodesViewSerializer(nodeslst, many=True)
        edgeslst = Edges.objects.all()
        edges_serializer = EdgesViewSerializer(edgeslst, many=True)

        return Response({
            "class": "GraphLinksModel",
            'nodeDataArray': nodes_serializer.data,
            'linkDataArray': edges_serializer.data,
        })

##### StepTest #####
@api_view(['GET', 'POST'])
def steptest(request):
    if request.method == 'GET':
        try:
            data = steptest_model()
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # try:
    #     steptest_model()
    #     return Response(status=status.)
    # except:
    #     return Response(status=500)