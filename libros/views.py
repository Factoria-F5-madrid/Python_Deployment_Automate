from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Libro
from categorias.models import Categoria
from .serializer import LibroSerializer

class VistasLibros():
    @api_view(['GET'])
    def ListaLibros(request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def CrearLibros(request):

        serializer = LibroSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def DetalleLibros(request, pk):
        try:
            libro = Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LibroSerializer(libro)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = LibroSerializer(libro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            libro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
