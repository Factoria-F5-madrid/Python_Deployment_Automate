from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializer import CategoriaSerializer

class VistasCategorias():
    @api_view(['GET'])
    def ListaCategorias(request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def crearCategorias(request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT', 'DELETE'])
    def DetalleCategorias(request, pk):
        try:
            categoria = Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CategoriaSerializer(categoria)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = CategoriaSerializer(categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            categoria.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)