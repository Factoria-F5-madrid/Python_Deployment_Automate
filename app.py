import streamlit as st
import datetime
import requests

st.sidebar.title('Menú')
st.sidebar.write('Bienvenidxs a mi librería')

st.title('Bienvenidxs a mi librería')
st.write('Estos son mis libros desde mi API:')

# Mostrar libros existentes
response = requests.get('http://127.0.0.1:8000/v1/libros')
if response.status_code == 200:
    libros = response.json()
    for libro in libros:
        st.write(f"Titulo: {libro['titulo']}")
        st.write(f"Categorías: {', '.join([str(categoria) for categoria in libro['categorias']])}")
        if st.button(f"Ver detalle {libro['id']}"):
            st.write(libro)
        if st.button(f"Borrar {libro['id']}"):
            delete_response = requests.delete(f"http://127.0.0.1:8000/v1/libros/{libro['id']}")
            if delete_response.status_code == 204:
                st.write(f"Libro {libro['id']} borrado")
            else:
                st.write(f"No se pudo borrar el libro {libro['id']}")
else:
    st.write('No se encontraron libros')

# Obtener categorías existentes
categorias_response = requests.get('http://127.0.0.1:8000/v1/categorias')
categorias = []
if categorias_response.status_code == 200:
    categorias = categorias_response.json()

# Formulario para crear un nuevo libro
st.sidebar.title('Crear nuevo libro')
titulo = st.sidebar.text_input('Título')
autor = st.sidebar.text_input('Autor')
isbn = st.sidebar.text_input('ISBN')
fecha_publicacion = st.sidebar.date_input(
    'Fecha de publicación', 
    min_value=datetime.date(1, 1, 1),
    max_value=datetime.date.today()
)
categorias_seleccionadas = st.sidebar.multiselect(
    'Categorías', [categoria['id'] for categoria in categorias], format_func=lambda id: next(c['nombre_categoria'] for c in categorias if c['id'] == id)
)

if st.sidebar.button('Crear libro'):
    nuevo_libro = {
        'titulo': titulo,
        'autor': autor,
        'isbn': isbn,
        'fecha_publicacion': str(fecha_publicacion),
        'categorias': categorias_seleccionadas
    }
    create_response = requests.post('http://127.0.0.1:8000/v1/libros/crear', json=nuevo_libro)
    if create_response.status_code == 201:
        st.sidebar.write('Libro creado exitosamente')
    else:
        st.sidebar.write('Error al crear el libro!')