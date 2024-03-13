# API inmobiliaria Bonpland
> [!NOTE]
> Este proyecto aun está en desarrollo.

<picture>
    <a href="https://dev-inmobiliaria.netlify.app">
        <img src="/img/InmobiliariaBonplandBanner.png">
    </a>
</picture>

Este proyecto hace parte de una iniciativa personal, esto implica que dicha inmobiliaria es una **institución ficticia**. El motivo que impulsa el desarrollo de este proyecto es el de mejorar mis habilidades técnicas en el desarrollo backend con Python, partiendo de lo más básico hasta temas avanzados como implementar un sistema de tareas en segundo plano o la implementación de patrones de arquitectura y de diseño.

De esta manera se está simulando que la inmobiliaria es un cliente con una necesidad o problemática que desea solucionar a través de una aplicación web. Así comienza la iniciativa de este proyecto que parte del proceso de licitación de requerimientos, documentación, planificación, desarrollo y despliegue.

En este repositorio encontrarás el código fuente de la API para la plataforma de gestión de inmobiliaria Bonpland. Para desarrollar este API nos hemos apoyado de un marco de trabajo muy potente conocido como [Django Rest Framework](https://www.django-rest-framework.org/).

## 1. Descripción del proyecto

La inmobiliaria opera principalmente a través de sus oficinas físicas y busca aprovechar la tecnología para ampliar su presencia en el mercado digital. La creación de una plataforma en línea no solo mejorará su visibilidad sino también la eficiencia de sus servicios.

### 1.1. Características de los usuarios
El sistema de gestión de inmuebles contendrá dos tipos de usuarios:

- **Buscadores de Propiedad:** Estos son los usuarios que están buscando comprar, alquilar o arrendar un inmueble. Son los clientes potenciales para las propiedades listadas en la inmobiliaria.
- **Propietarios de Propiedad:** Estos son los propietarios de inmuebles que buscan vender, alquilar o arrendar sus propiedades a través de la inmobiliaria. Son los clientes que proporcionan el inventario de propiedades para la inmobiliaria.
- **Administradores:** Son los individuos que manejan la plataforma online de la inmobiliaria, pueden ser empleados de la misma que se encargan de administrar la plataforma web y las necesidades de los clientes (buscadores de propiedad o propietarios de propiedad).

### 1.2. Requerimientos funcionales
- Registro parcial de un usuario.
- Autenticación para usuarios.
- Activar una cuenta de usuario.
- Actualizar la información de un usuario.
- Eliminar un usuario.
- Restablecer contraseña.
- Confirmar número telefónico.
- Filtrado para la búsqueda de inmuebles.
- Guardado de inmuebles para usuarios.

### 1.3. Estructura
La estructura del proyecto es la siguiente:

```
└── 📁src
    └── 📁apps
    └── 📁settings
        └── 📁environments
            └── base.py
            └── local.py
            └── production.py
            └── test.py
        └── asgi.py
        └── constans.py
        └── urls.py
        └── wsgi.py
    └── 📁test
    └── manage.py
    └── pytest.ini
    └── requirements.txt
```

- **[src](./src/):** este es el directorio raíz del poryecto. Contiene todos los modulos, configuraciones  globales y pruebas del código.

- **[apps](./src/apps/):** este directorio contiene las aplicaciones Dajngo. Está dividido en varios subdirectorios, cada uno de los cuales representa un servicio o aplicación. Tambien podras encontras algunos ficheros auxiliares en donde cada servicio podra hacer uso de ellos respectivamente.

- **[settings](./src/settings/):** Contiene archivos de configuración para la API. Incluye configuraciones para los diferentes entornos de desarrollo, producción y pruebas, configuraciones de los punto finales de la API, configuraciones ASGI y WSGI, etc.

- **[test](./src/test/):** Contiene pruebas unitarias y de implementación del código de cada aplicación.

- **[manage.py](./src/manage.py):** esta es una utilidad de línea de comandos que te permite interactuar con tu proyecto Django de varias maneras.

- **[requirements.txt](./src/requirements.txt):** este archivo se utiliza para administrar dependencias para un proyecto de Python. Enumera todos los paquetes de Python de los que depende el proyecto.

- **[pytest.ini](./src/pytest.ini):** Este archivo contiene la configuración para pytest, un marco de prueba para Python.

## 2. Instalación en local

Primero debes clonar este repositorio utilizando el siguiente comando en tu consola.

```bash
  git clone https://github.com/CodingFlashOR/api-inmobiliaria.git
```

> [!NOTE]
> Asegúrese que Python esté instalado en su sistema operativo.

- **Paso 1 (instalar dependencias):** Para instalar las teconologias y paquetes que usa el proyecto usa el siguiente comando. Asegurate estar en el directotio raíz.

    ```bash
    pip install -r "requirements.txt"
    ```

- **Paso 2 (Instalar configuración pre-commit):** Este repositorio contiene unas reglas necesarias para  mantener la calidad del código, antes de realizar un `commit`se validara que los archivos estan correctamente formateados segun el estandar [PEP8](https://peps.python.org/pep-0008/), también se validará que los commits sigan el estándar [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). Para iniciar estas reglas debes ejecutar el siguiente comando, 

    ```bash
    pre-commit install
    pre-commit install --hook-type commit-msg
    ```

- **Paso 3 (configurar variables de entorno):** Crea un archivo con el nombre _.env_ dentro del directorio raíz. Dentro de este archivo se definiran todas las variables de entorno de este proyecto.

    ```.env
    ENVIRONMENT_STATUS='development'
    KEY_DJANGO='value'
    ```

    El valor de la variable `KEY_DJANGO` lo puedes obtener ejecutando los siguientes comandos. El ultimo comando retorna el valor de la variable que deberas copiar en el archivo _.env_.

    ```bash
    python3
    from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()); exit()
    ```

- **Paso 4 (realizar migraciones):** Migramos los modelos del proyecto necesarios para el funcionamiento del servidor con el siguiente comando.

    ```bash
    python3 manage.py migrate
    ```

- **Paso 5 (Iniciar el servidor):** Para iniciar el servidor de manera local ejecuta el siguiente comando.

    ```bash
    python3 manage.py runserver
    ```

De esta manera podrás usar todas las funcionalidades que este proyecto tiene para ofrecer. Es importante que hayas seguido todos los pasos explicados en el orden establecido.

## 3. Tests
Para correr las pruebas unitarias del código ejecuta el siguiente comando.

```bash
pytest
```

## 4. Documentación
| Título | Descripción | 
|----------|----------|
| [Especifcación de requerimientos](https://drive.google.com/file/d/1rHrYdVJ7h1wPVbSSrLhgfYliH-DhmyL-/view?usp=drive_link) | Este documento detalla los requerimientos funcionales, no funcionales y el comportamiento de las diferentes interfaces del sistema. |
| [Base de datos]()   | Este documento proporciona una visión detallada de la estructura de la base de datos utilizada en el proyecto. |
| [Documentación de la API](https://backend-inmobiliaria-dev-rgzp.2.us-1.fl0.io/api/schema/swagger-ui/) | Esta es la documentación para la API del proyecto, que incluye detalles sobre los endpoints disponibles y los datos que se pueden enviar y recibir. |

## 6. Colaboradores
| Nombre | Rol | 
|----------|----------|
| [Carlos Andres Aguirre Ariza](https://github.com/The-Asintota) | Backend |
