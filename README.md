# API inmobiliaria Bonpland
> [!NOTE]
> Este proyecto aun está en desarrollo.

<div>
    <a href="https://carlosandresaguirreariza.pythonanywhere.com/">
        <img src="/images/InmobiliariaBonplandBanner.png">
    </a>
</div>

En este repositorio encontrarás el código fuente de la API para la plataforma de gestión de inmobiliaria Bonpland, puedes consultar la documentación completa [aquí](https://carlosandresaguirreariza.pythonanywhere.com/) o visitar el sitio web [aquí](https://dev-inmobiliaria.netlify.app/).

## 1. Descripción del proyecto

La inmobiliaria opera principalmente a través de sus oficinas físicas y busca aprovechar la tecnología para tener presencia en el mercado digital. La creación de una plataforma en línea no solo mejorará su visibilidad sino también la eficiencia de sus servicios.

El sistema de gestión inmobiliaria se integra como una extensión de las operaciones tradicionales de la inmobiliaria. La plataforma en línea le permitirá ampliar su alcance y ofrecer servicios en línea a sus clientes sin reemplazar por completo las interacciones presenciales en sus oficinas físicas. La perspectiva del producto se centra en proporcionar una experiencia en línea atractiva y eficiente para los usuarios finales, al tiempo que facilita la administración y el flujo de trabajo para los administradores de la inmobiliaria.

### 1.1. Características de los usuarios
El sistema de gestión de inmuebles contendrá dos tipos de usuarios:

- **Buscador de inmuebles:** Estos son los usuarios que buscan comprar o arrendar un inmueble. Son uno de los clientes a los cuales la inmobiliaria ofrece sus servicios.
- **Propietario de inmuebles:** Estos son los propietarios de inmuebles que buscan poner a la venta o en arriendo sus propiedades a través de la inmobiliaria. Son los clientes que proporcionan el inventario de propiedades para la inmobiliaria.
- **Administrador:** Son los individuos que manejan la plataforma online de la inmobiliaria, pueden ser empleados de la misma que se encargan de administrar la plataforma web y las necesidades de los clientes (buscadores y propietarios de inmuebles).

### 1.2. Requerimientos funcionales
- Registro de usuarios.
- Autenticación.
- Actualizar la información de un usuario.
- Eliminar un usuario.
- Restablecer contraseña.
- Confirmar número telefónico.
- Activación de cuenta de usuarios vía correo electrónico.
- Filtrado para la búsqueda de inmuebles.
- Guardado de inmuebles para usuarios.
- Funcionalidades para administradores.
- Sistema de envío de notificaciones para usuarios.

## 2. Tecnologías
<div>
    <img src="/images/TechnologiesBackendIB.png">
</div>

## 3. Instalación del proyecto
> [!NOTE]
> Asegúrese que Python 3.10 y [poetry](https://python-poetry.org/docs/#installation) esté instalado en su sistema operativo.

Primero debes seguir las siguientes instrucciones y dependiendo de que manera quieres realizar la instalación seguiras los pasos para instalar el proyecto de manera manual o utilizando Docker.

- **Clonar repositorio:** Para clonar este repositorio ejecuta los siguientes comandos.
    
    ```bash
    git clone https://github.com/CodingFlashOR/backend-inmobiliaria.git
    cd backend-inmobiliaria
    ```
    
- **Crear y activar entorno virtual:** Creares un entorno virtual con el siguiente comando, en este entorno instalaremos todas las dependencias de este proyecto.
    
    ```bash
    poetry shell
    ```

- **Configurar variables de entorno:** Crea un archivo con el nombre _.env_ dentro del directorio _backend-inmobiliaria_. En este archivo se definiran todas las variables de entorno de este proyecto. Las variables que se deben configurar son las siguientes.

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
    poetry install
    ```
    
- **Paso 2 (realizar migraciones):** Migramos los modelos del proyecto necesarios para el funcionamiento del servidor con el siguiente comando.
    
    ```bash
    python3 api_inmobiliaria/manage.py migrate --settings=settings.environments.development
    ```

- **Paso 3 (iniciar el servidor):** Para iniciar el servidor de manera local ejecuta el siguiente comando.
    
    ```bash
    python3 api_inmobiliaria/manage.py runserver --settings=settings.environments.development
    ```
    
### 3.2. Instalación con Docker

- **Paso 1 (Construir imagen):** para construir la imagen del contenedor de este pryecto debes ejecutar el siguiente comando.
    
    ```bash
    docker build -t api_inmobiliaria .
    ```
    
- **Paso 2 (Correr imagen):** para iniciar el contenedor de este pryecto debes ejecutar el siguiente comando.
    
    ```bash
    docker run -e ENVIRONMENT=development -p 8000:8000 api_inmobiliaria
    ```
    
De esta manera podrás usar todas las funcionalidades que este proyecto tiene para ofrecer. Es importante que hayas seguido todos los pasos explicados en el orden establecido.

## 4. Tests
Para correr las pruebas del proyecto debes ejecutar el siguiente comando.

```bash
pytest
```

## 5. Contributores
Si está interesado en contribuir a este proyecto, consulte nuestra guía [CONTRIBUTING](CONTRIBUTING.md) para obtener información sobre cómo comenzar. Proporciona pautas sobre cómo configurar su entorno de desarrollo, proponer cambios y más. ¡Esperamos sus contribuciones!

## 6. Documentación
| Título | Descripción | 
|----------|----------|
| [Especifcación de requerimientos](https://drive.google.com/file/d/1rHrYdVJ7h1wPVbSSrLhgfYliH-DhmyL-/view?usp=drive_link) | Este documento detalla los requerimientos funcionales, no funcionales y el comportamiento de las diferentes interfaces del sistema. |
| [Base de datos]()   | Este documento proporciona una visión detallada de la estructura de la base de datos utilizada en el proyecto. |
| [Documentación de la API](https://carlosandresaguirreariza.pythonanywhere.com/) | Esta es la documentación para la API del proyecto, que incluye detalles sobre los endpoints disponibles y los datos que se pueden enviar y recibir. |

## 7. Repositorios relacionados
- [Repositorio Principal](https://github.com/CodingFlashOR#11-inmobiliaria-bonpland).
- [Repositorio Frontend](https://github.com/CodingFlashOR/frontend-inmobiliaria/tree/dev).

## 8. Colaboradores
A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles | 
|----------|:--------:|:--------:|
| Yoana Avaro | [LinkedIn](https://www.linkedin.com/in/yoana-avaro/) | Diseño UX/UI |
| Maria Fuentes | [LinkedIn](https://www.linkedin.com/in/maria-fuentes-112920256/) - [GitHub](https://github.com/Mmff07) - [Behance](https://www.behance.net/mariafuentes22) | Diseño UX/UI |
| Flor Rivas Luna | [LinkedIn](https://www.linkedin.com/in/floridesign/) - [GitHub](https://github.com/FlorRivas) - [Behance](https://www.behance.net/floridesign) | Diseño UX/UI |
| Ignacio Nicolas Basilio Buracco | [GitHub](https://github.com/NachoBasilio) - [LinkedIn](https://www.linkedin.com/in/ignacio-nicolas-basilio-buracco/) | Frontend |
| Jose Lozada | [GitHub](https://github.com/lozada07) | Frontend |
| Carlos Andres Aguirre Ariza | [GitHub](https://github.com/The-Asintota) - [LinkedIn](https://www.linkedin.com/in/carlosaguirredev/) | Backend - Frontend |
| Gabriela Patiño | [GitHub](https://github.com/Gabyp05) - [LinkedIn](https://www.linkedin.com/in/gabyp05/) | QA |
| Carolina Pascua | [GitHub](https://github.com/CarolinaPascua) - [LinkedIn](https://www.linkedin.com/in/carolinalidiapascua/) | QA |
