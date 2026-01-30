from django.db import models
from categorias.models import Categoria

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    fecha_publicacion = models.DateField()
    
    categorias = models.ManyToManyField(Categoria, related_name='categorias')

    def __str__(self):
        return self.titulo