# Usa la imagen base de Python 3.12 en su versión "slim" (más liviana)
# "slim" significa que viene con menos paquetes preinstalados para reducir el tamaño
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor como /app
# Todos los comandos siguientes se ejecutarán desde este directorio
WORKDIR /app

# Actualiza la lista de paquetes disponibles del sistema operativo
# && encadena comandos - si uno falla, se detiene la ejecución
RUN apt-get update \
# Instala paquetes del sistema operativo necesarios para compilar mysqlclient
# mysqlclient es una dependencia de Python que requiere compilación en C
&& apt-get install -y --no-install-recommends \
    build-essential \              
    # Conjunto de herramientas de compilación esenciales:
    # - make: para ejecutar makefiles
    # - gcc: compilador de C/C++
    # - libc6-dev: librerías de desarrollo de C
    # Sin esto, no se pueden compilar extensiones de Python en C
    gcc \                          
    # Compilador de C/C++ específicamente
    # mysqlclient tiene código en C que debe compilarse
    # Aunque está incluido en build-essential, se especifica explícitamente
    python3-dev \                  
    # Headers y archivos de desarrollo de Python
    # Contiene Python.h y otras cabeceras necesarias
    # para que las extensiones en C puedan "hablar" con Python
    # Sin esto, mysqlclient no puede integrarse con Python
    pkg-config \                   
    # Herramienta que ayuda a encontrar librerías instaladas
    # Proporciona información sobre dónde están las librerías
    # y qué flags de compilación usar
    # mysqlclient lo usa para encontrar las librerías de MySQL
    default-libmysqlclient-dev \   
    # Librerías de desarrollo del cliente MySQL
    # Contiene archivos .h (headers) y .so (librerías compartidas)
    # Permite que mysqlclient se comunique con bases de datos MySQL
    # Es la "interfaz" entre Python y MySQL
    libmariadb-dev \               
    # Librerías de desarrollo de MariaDB (fork de MySQL)
    # MariaDB es compatible con MySQL pero tiene mejores drivers
    # Proporciona una alternativa más moderna para la conexión
    # Muchas veces funciona mejor que las librerías nativas de MySQL
    # Operaciones de limpieza para reducir el tamaño final de la imagen Docker
    && apt-get clean \                 
    # Elimina archivos temporales del gestor de paquetes apt
    # Borra el caché de paquetes descargados (/var/cache/apt/archives/)
    # Estos archivos ya no son necesarios después de la instalación
    && rm -rf /var/lib/apt/lists/*     
    # Elimina las listas de paquetes disponibles
    # Estas listas se descargan con 'apt-get update'
    # Ocupan espacio y no son necesarias en el contenedor final
    # Pueden regenerarse si se necesitan con otro 'apt-get update'

# Copia el archivo requirements.txt desde tu máquina al directorio /app del contenedor
# El punto (.) significa "directorio actual" dentro del contenedor (/app)
COPY requirements.txt .

# Actualiza pip a la última versión disponible
RUN pip install --upgrade pip \
    # Instala todas las dependencias listadas en requirements.txt
    # --no-cache-dir evita guardar caché para reducir el tamaño de la imagen
    && pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio actual (tu proyecto) al contenedor
# Primer punto: directorio actual de tu máquina
# Segundo punto: directorio actual del contenedor (/app)
COPY . .

# Informa que el contenedor expondrá el puerto 8000
# Esto es solo documentación - no abre el puerto automáticamente
EXPOSE 8000

# Comando que se ejecutará cuando el contenedor inicie
# Inicia el servidor de desarrollo de Django en el puerto 8000
# 0.0.0.0 permite conexiones desde cualquier IP (necesario para Docker)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]