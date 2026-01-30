from django.urls import path
from .views import VistasCategorias

urlpatterns = [
    path('', VistasCategorias.ListaCategorias, name='lista-categoria'),
    path('crear', VistasCategorias.crearCategorias, name='crear-categoria'),
    path('<int:pk>', VistasCategorias.DetalleCategorias, name='detalle-categoria'),
]