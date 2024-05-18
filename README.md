# API inmobiliaria Bonpland
> [!NOTE]
> Este proyecto aun está en desarrollo.

<div>
    <a href="https://carlosandresaguirreariza.pythonanywhere.com/">
        <img src="/images/InmobiliariaBonplandBanner.png">
    </a>
</div>

En este repositorio encontrarás el código fuente de la API para la plataforma de gestión de inmobiliaria Bonpland, puedes consultar la documentación completa [aquí](https://carlosandresaguirreariza.pythonanywhere.com/).

## 1. Descripción del proyecto

La inmobiliaria opera principalmente a través de sus oficinas físicas y busca aprovechar la tecnología para ampliar su presencia en el mercado digital. La creación de una plataforma en línea no solo mejorará su visibilidad sino también la eficiencia de sus servicios.

### 1.1. Características de los usuarios
El sistema de gestión de inmuebles contendrá dos tipos de usuarios:

- **Buscador de inmuebles:** Estos son los usuarios que están buscando comprar, alquilar o arrendar un inmueble. Son los clientes potenciales para las propiedades listadas en la inmobiliaria.
- **Propietario de inmuebles:** Estos son los propietarios de inmuebles que buscan vender, alquilar o arrendar sus propiedades a través de la inmobiliaria. Son los clientes que proporcionan el inventario de propiedades para la inmobiliaria.
- **Administrador:** Son los individuos que manejan la plataforma online de la inmobiliaria, pueden ser empleados de la misma que se encargan de administrar la plataforma web y las necesidades de los clientes (buscadores de propiedad o propietarios de propiedad).

### 1.2. Requerimientos funcionales
- Registro de un usuarios.
- Autenticación para usuarios.
- Actualizar la información de un usuario.
- Eliminar un usuario.
- Confirmar número telefónico.
- Activación de cuenta de usuarios vía correo electrónico.
- Restablecer contraseña vía correo electrónico.
- Filtrado para la búsqueda de inmuebles.
- Guardado de inmuebles para usuarios.
- Funcionalidades para administradores.

### 1.3. Estructura
La estructura del proyecto es la siguiente:

```
└── 📁src
    └── 📁apps
    └── 📁settings
        └── 📁environments
            └── base.py
            └── development.py
            └── production.py
            └── testing.py
        └── asgi.py
        └── urls.py
        └── wsgi.py
    └── 📁tests
    └── manage.py
    └── pytest.ini
    └── requirements.txt
```

- **[src](./src/):** este es el directorio raíz del poryecto. Contiene todos los modulos, configuraciones  globales y pruebas del código.

- **[apps](./src/apps/):** este directorio contiene las aplicaciones Dajngo. Está dividido en varios subdirectorios, cada uno de los cuales representa un servicio o aplicación. Tambien podras encontras algunos ficheros auxiliares en donde cada servicio podra hacer uso de ellos respectivamente.

- **[settings](./src/settings/):** Contiene archivos de configuración para la API. Incluye configuraciones para los diferentes entornos de desarrollo, producción y pruebas, configuraciones de los punto finales de la API, configuraciones ASGI y WSGI, etc.

- **[tests](./src/tests/):** Contiene pruebas unitarias y de implementación del código de cada aplicación.

- **[manage.py](./src/manage.py):** esta es una utilidad de línea de comandos que te permite interactuar con tu proyecto Django de varias maneras.

- **[requirements.txt](./src/requirements.txt):** este archivo se utiliza para administrar dependencias para un proyecto de Python. Enumera todos los paquetes de Python de los que depende el proyecto.

- **[pytest.ini](./src/pytest.ini):** Este archivo contiene la configuración para pytest, un marco de prueba para Python.

## 2. Tecnologías
<div>
    <img src="/images/TechnologiesBackendIB.png">
</div>

## 3. Instalación del proyecto
> [!NOTE]
> Asegúrese que Python 3.11.5 esté instalado en su sistema operativo.

Primero debes seguir las siguientes instrucciones y dependiendo de que manera quieres realizar la instalación seguiras los pasos para instalar el proyecto de manera manual o utilizando Docker.

- **Clonar repositorio:** Para clonar este repositorio ejecuta los siguientes comandos.
    
    ```bash
    git clone https://github.com/CodingFlashOR/api-inmobiliaria.git
    cd api-inmobiliaria
    ```
    
- **Crear y activar entorno virtual:** Creares un entorno virtual con el siguiente comando, en este entorno instalaremos todas las dependencias de este proyecto.
    
    ```bash
    python3 -m venv <nombre_del_entorno>
    ```
    
    Por ultimo activamos el entorno con el siguiente comando.
    
    ```bash
    # Linux y macOS
    source <nombre_del_entorno>/bin/activate
    
    # Windows
    .<nombre_del_entorno>\Scripts\activate
    ```
    
- **Configurar variables de entorno:** Crea un archivo con el nombre _.env_ dentro del directorio _src_. En este archivo se definiran todas las variables de entorno de este proyecto. Las variables que se deben configurar son las siguientes.

    ```.env
    # DJANGO
    KEY_DJANGO=<value>

    # SMTP settings
    EMAIL_HOST_USER=<tu correo electrónico>
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_PASSWORD=<contraseña de aplicación de tu correo>
    EMAIL_PORT=587
    EMAIL_USE_TLS=true
    ```

    El valor de la variable `KEY_DJANGO` lo puedes obtener ejecutando los siguientes comandos. Primero iniciamos el intérprete de Python.

    ```bash
    python3
    ```

    El siguiente comando te va retornar el valor de `KEY_DJANGO` que deberas copiar en el archivo _.env_.

    ```bash
    from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()); exit()
    ```

    Para el envío de mensajes a través de correo electrónico tienes que tener una contraseña de aplicación que permita al sistema de gestión inmobiliario autenticarse y poder utilizar el servicio de mensajería.

### 3.1. Instalación manual

- **Paso 1 (instalar dependencias):** Para instalar las teconologias y paquetes que usa el proyecto usa el siguiente comando. Asegurate estar en el directotio raíz.
    
    ```bash
    pip install -r "requirements.txt"
    ```
    
- **Paso 2 (realizar migraciones):** Migramos los modelos del proyecto necesarios para el funcionamiento del servidor con el siguiente comando.
    
    ```bash
    python3 src/manage.py migrate --settings=settings.environments.development
    ```

- **Paso 3 (iniciar el servidor):** Para iniciar el servidor de manera local ejecuta el siguiente comando.
    
    ```bash
    python3 src/manage.py runserver --settings=settings.environments.development
    ```
    
### 3.2. Instalación con Docker

- **Paso 1 (Construir imagen):** para construir la imagen del contenedor de este pryecto debes ejecutar el siguiente comando.
    
    ```bash
    docker build -t api-inmobiliaria .
    ```
    
- **Paso 2 (Correr imagen):** para iniciar el contenedor de este pryecto debes ejecutar el siguiente comando.
    
    ```bash
    docker run -p 8000:8000 api-inmobiliaria
    ```
    
De esta manera podrás usar todas las funcionalidades que este proyecto tiene para ofrecer. Es importante que hayas seguido todos los pasos explicados en el orden establecido.

## 4. Tests
Para correr las pruebas del proyecto debes ejecutar el siguiente comando.

```bash
pytest src/tests/
```

## 5. Contributores
Si está interesado en contribuir a este proyecto, consulte nuestra guía [CONTRIBUTING](CONTRIBUTING.md) para obtener información sobre cómo comenzar. Proporciona pautas sobre cómo configurar su entorno de desarrollo, proponer cambios y más. ¡Esperamos sus contribuciones!

## 6. Documentación
| Título | Descripción | 
|----------|----------|
| [Especifcación de requerimientos](https://drive.google.com/file/d/1rHrYdVJ7h1wPVbSSrLhgfYliH-DhmyL-/view?usp=drive_link) | Este documento detalla los requerimientos funcionales, no funcionales y el comportamiento de las diferentes interfaces del sistema. |
| [Base de datos]()   | Este documento proporciona una visión detallada de la estructura de la base de datos utilizada en el proyecto. |
| [Documentación de la API](https://backend-inmobiliaria-dev-rgzp.2.us-1.fl0.io/api/schema/swagger-ui/) | Esta es la documentación para la API del proyecto, que incluye detalles sobre los endpoints disponibles y los datos que se pueden enviar y recibir. |

## 7. Repositorios relacionados
- [Repositorio Principal](https://github.com/CodingFlashOR#11-inmobiliaria-bonpland).
- [Repositorio Frontend](https://github.com/CodingFlashOR/frontend-inmobiliaria/tree/dev).

## 8. Colaboradores
A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles | 
|----------|:--------:|:--------:|
| Yoana Avaro | <a href="https://www.linkedin.com/in/yoana-avaro/" target="_blank">LinkedIn</a> | Diseño UX/UI |
| Maria Fuentes | <a href="https://www.linkedin.com/in/maria-fuentes-112920256/" target="_blank">LinkedIn</a> - <a href="https://github.com/Mmff07" target="_blank">Git Hub</a> - <a href="https://www.behance.net/mariafuentes22" target="_blank">Behance</a> | Diseño UX/UI |
| Ignacio Nicolas Basilio Buracco | <a href="https://github.com/NachoBasilio" target="_blank">Git Hub</a> - <a href="https://www.linkedin.com/in/ignacio-nicolas-basilio-buracco/" target="_blank">LinkedIn</a> | Frontend |
| Jose Lozada | <a href="https://github.com/lozada07" target="_blank">Git Hub</a> - <a href="" target="_blank">LinkedIn</a> | Frontend |
| Carlos Andres Aguirre Ariza | <a href="https://github.com/The-Asintota" target="_blank">Git Hub</a> - <a href="https://www.linkedin.com/in/carlosaguirredev/" target="_blank">LinkedIn</a> | Backend - Frontend |
| Gabriela Patiño | <a href="https://github.com/Gabyp05" target="_blank">Git Hub</a> - <a href="https://www.linkedin.com/in/gabyp05/" target="_blank">LinkedIn</a> | QA |
| Carolina Pascua | <a href="https://github.com/CarolinaPascua" target="_blank">Git Hub</a> - <a href="https://www.linkedin.com/in/carolinalidiapascua/" target="_blank">LinkedIn</a> | QA |
