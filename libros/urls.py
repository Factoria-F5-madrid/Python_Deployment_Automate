from django.urls import path
from .views import VistasLibros

urlpatterns = [
    path('', VistasLibros.ListaLibros, name="Lista_libros"),
    path('crear', VistasLibros.CrearLibros, name="crear_libros"),
    path('<int:pk>', VistasLibros.DetalleLibros, name="detalle_libros"),
]