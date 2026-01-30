from rest_framework import serializers
from .models import Libro
from categorias.models import Categoria

class LibroSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True
    )
    class Meta:
        model = Libro
        fields = '__all__'