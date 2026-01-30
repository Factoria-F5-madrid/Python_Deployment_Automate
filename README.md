# CI/CD: Publicación automática de la imagen en Docker Hub con GitHub Actions

En esta guía, configuraremos un flujo de trabajo de Integración Continua y Despliegue Continuo (CI/CD) utilizando GitHub Actions. El objetivo es automatizar la construcción y publicación de nuestra imagen de Docker en Docker Hub cada vez que realicemos un `push` a la rama `main` u otra que definamos, en este caso `ci-cd-django-restf`.

## Prerrequisitos

Antes de comenzar, necesitamos:
1.  Un repositorio de GitHub donde reside este proyecto.
2.  Una cuenta en [Docker Hub](https://hub.docker.com/).

## Paso 1: Generar un Token de Acceso en Docker Hub

El flujo de trabajo de GitHub Actions necesita credenciales para iniciar sesión en Docker Hub. En lugar de usar nuestra contraseña, crearemos un Token de Acceso por seguridad.

1.  Iniciamos sesión en Docker Hub.
2.  Vamos a **Account Settings** -> **Personal access tokens**.
![alt text](./assets/acc-settings.PNG)
![alt text](./assets/acc-token.PNG)
3.  Hacemos clic en **Generate New Token**.
![alt text](./assets/acc-gen.PNG)
4.  Le damos un nombre descriptivo (por ejemplo, `github-actions-token`) y le asignamos permisos de **Read, Write & Delete**.
![alt text](./assets/acc-cre.PNG)
5.  Hacemos clic en **Generate**.
6.  **¡Importante!** Copiamos el token y lo guardamos en un lugar seguro. No podremos volver a verlo después de cerrar esta ventana.
![alt text](./assets/token.PNG)

## Paso 2: Configurar los Secrets en el Repositorio de GitHub

Ahora, vamos a almacenar de forma segura nuestro nombre de usuario y el token de acceso en nuestro repositorio de GitHub.

1.  En el repositorio, vamos a **Settings** -> **Secrets and variables** -> **Actions**.
![alt text](./assets/sett.PNG)
![alt text](./assets/sv.PNG)
2.  Hacemos clic en **New repository secret** para agregar los siguientes dos secretos:
    *   **`DOCKERHUB_USERNAME`**: Nuestro nombre de usuario de Docker Hub.
    *   **`DOCKERHUB_TOKEN`**: El token de acceso que generamos en el paso anterior.
![alt text](./assets/rep-s.PNG)
![alt text](./assets/us.PNG)
![alt text](./assets/tok.PNG)

## Paso 3: Crear el Flujo de Trabajo (Workflow) de GitHub Actions

A continuación, crearemos el archivo que define el flujo de trabajo.

1.  En la raíz de nuestro proyecto, creamos una nueva estructura de directorios: `.github/workflows/`.
2.  Dentro de esa carpeta, creamos un nuevo archivo llamado `docker-publish.yml`.
3.  Copiamos y pegamos el siguiente contenido en el archivo `docker-publish.yml`:

```yaml
name: Publicar Imagen de Docker en Docker Hub

# Este flujo de trabajo se ejecuta cada vez que hay un push a la rama 'main'
on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    # Usamos la última versión de Ubuntu para ejecutar nuestro trabajo
    runs-on: ubuntu-latest

    steps:
      # 1. Obtenemos el código del repositorio
      - name: Checkout del código
        uses: actions/checkout@v4

      # 2. Iniciamos sesión en Docker Hub
      - name: Iniciar sesión en Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 3. Construimos la imagen y la publicamos
      - name: Construir y publicar la imagen de Docker
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/python_deployment_automate:v1
```

### Explicación del Flujo de Trabajo

-   **`on: push: branches: [ main ]`**: Define que el flujo de trabajo se activará con cada `push` a la rama `main`.
-   **`jobs: build-and-push`**: Define un trabajo llamado `build-and-push` que se ejecutará en un entorno `ubuntu-latest`.
-   **`steps`**:
    -   **`actions/checkout@v4`**: Descarga el código fuente de nuestro repositorio para que el flujo de trabajo pueda usarlo.
    -   **`docker/login-action@v3`**: Inicia sesión en Docker Hub utilizando los secretos que configuramos anteriormente.
    -   **`docker/build-push-action@v5`**: Esta es la acción principal.
        -   `context: .`: Le dice que el contexto de construcción de Docker (donde se encuentra el `Dockerfile`) es la raíz del proyecto.
        -   `push: true`: Indica que después de construir la imagen, debe publicarla en el registro.
        -   `tags: ${{ secrets.DOCKERHUB_USERNAME }}/todo-server-app:latest`: Etiqueta la imagen con nuestro nombre de usuario de Docker Hub, el nombre de la aplicación y la etiqueta `latest`.

## Paso 4: ¡A Probarlo!

1.  Guardamos el archivo `docker-publish.yml`.
2.  Hacemos `commit` y `push` de los cambios a la rama `main`.
3.  Vamos a la pestaña **Actions** en nuestro repositorio de GitHub. Veremos que nuestro flujo de trabajo "Publicar Imagen de Docker en Docker Hub" se está ejecutando.
4.  Una vez que el trabajo finalice con éxito, podemos ir a nuestro perfil en Docker Hub y veremos la imagen `todo-server-app` actualizada en nuestro repositorio.

A partir de ahora, cada vez que hagamos un `push` a `main`, la imagen de Docker se reconstruirá y actualizará automáticamente.
