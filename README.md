# API inmobiliaria Bonpland
> [!NOTE]
> Este proyecto aun está en desarrollo.

<div>
    <img src="/images/InmobiliariaBonplandBanner.png">
</div>

En este repositorio encontrarás el código fuente de la API para la plataforma de gestión de inmobiliaria Bonpland, puedes consultar la documentación completa [aquí](https://carlosandresaguirreariza.pythonanywhere.com/) o visitar el sitio web [aquí](https://main-inmobiliaria.netlify.app/).

## 1. Descripción del proyecto
La plataforma web se integra como una **extensión** de las operaciones tradicionales de la Inmobiliaria Bonpland. Esta plataforma en línea permitirá a la inmobiliaria ampliar su alcance y ofrecer servicios de manera digital, sin reemplazar por completo las interacciones presenciales en sus oficinas físicas. La perspectiva del producto se centra en proporcionar una experiencia en línea atractiva y eficiente para los usuarios finales, incluyendo paneles de búsqueda por filtros, al tiempo que facilita la administración y el flujo de trabajo para los empleados de la inmobiliaria. La plataforma permitirá a las constructoras y agentes inmobiliarios **gestionar proyectos o inmuebles**, mejorar la comunicación y coordinación entre todas las partes, y optimizar los procesos operativos para aumentar la eficiencia y reducir errores.

### 1.1. Características de los usuarios
El sistema de gestión de inmuebles está diseñado para atender a tres tipos principales de usuarios, cada uno con diferentes razones o motivaciones por las cuales utilizarían el sistema y lo que esperan lograr con su uso.

- **Buscadores:** Estos son los usuarios que buscan invertir en proyectos inmobiliarios de constructoras o adquirir inmuebles. Pueden ser personas individuales, parejas, familias, inversores o empresas.
- **Entidades inmobiliarias:** Estos usuarios representan a constructoras e inmobiliarias, dedicados a ofrecer productos inmobiliarios a través de la plataforma. Las inmobiliarias pueden gestionar tanto casas como departamentos, disponibles para la venta o alquiler. Por su parte, las constructoras se encargan de gestionar proyectos inmobiliarios en diversas etapas: desde la fase de planificación hasta la construcción y entrega, que pueden estar en planos, en proceso de construcción o listos para entrega inmediata.
- **Administradores:** Estos son los empleados de la inmobiliaria responsable de administrar y mantener la plataforma. Su función es garantizar que el sistema funcione sin problemas y que tanto los usuarios buscadores como las constructoras puedan utilizar la plataforma de manera efectiva.

### 1.2. Requerimientos funcionales
- Registro de usuarios.
- Sistema de autenticación con JWT.
- Actualizar la información de perfil para usuarios.
- Eliminar cuenta.
- Activación de la cuenta.
- Restablecer contraseña.
- Confirmación de un número telefónico.
- Sistema de filtros de búsqueda para inmuebles.
- Funcionalidades para administradores.
- Sistema de envío de notificaciones para usuarios.
- Sistema de envío de correos electrónicos.
- Gestión de permisos de usuarios.

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
    
- **Paso 2 (realizar migraciones):** Las migraciones son archivos que registran y aplican cambios en la estructura de la base de datos, como crear o modificar tablas y campos, asegurando que la base de datos esté sincronizada con los modelos definidos en el código. Migramos los modelos del proyecto con el siguiente comando.
    
    ```bash
    python3 api_inmobiliaria/manage.py migrate --settings=settings.environments.development
    ```

- **Paso 3 (configurar grupo de usuarios):** Un grupo de usuarios se refiere a una entidad dentro de un sistema o aplicación que agrupa a varios usuarios bajo un mismo conjunto de permisos, roles o privilegios. Esto se utiliza para simplificar la gestión de acceso y permisos en sistemas donde hay múltiples usuarios. Para crear los grupos configurados paraeste proyecto ejecuta el siguiente comando.
    
    ```bash
    python3 api_inmobiliaria/manage.py create_user_groups --settings=settings.environments.development
    ```

- **Paso 4 (iniciar el servidor):** Para iniciar el servidor de manera local ejecuta el siguiente comando.
    
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
| [Especifcación de requerimientos](https://writer.zoho.com/writer/open/gvaj1411213d7d4bb4c818860a3bea679ecbb) | Este documento detalla los requerimientos funcionales, no funcionales y el comportamiento de las diferentes interfaces del sistema. |
| [Base de datos](https://app.diagrams.net/?title=EsquemaDB.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1uJAsYcVnTEviwOq5JZ_q_2VWnpvgPfBd%26export%3Ddownload)   | Esquema de la base de datos del proyecto. |
| [Documentación de la API](https://carlosandresaguirreariza.pythonanywhere.com/) | Esta es la documentación para la API del proyecto, que incluye detalles sobre los endpoints disponibles y los datos que se pueden enviar y recibir. |

## 7. Repositorios relacionados
- [Repositorio Principal](https://github.com/CodingFlashOR#11-inmobiliaria-bonpland).
- [Repositorio Frontend](https://github.com/CodingFlashOR/frontend-inmobiliaria/tree/dev).

## 8. Colaboradores
A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles | 
|----------|:--------:|:--------:|
| Lucas A Bravi | [LinkedIn](https://www.linkedin.com/in/lucasandr%C3%A9sbravi/) - [Portafolio](https://lucasbravidi1062b1.myportfolio.com/) | Diseño UX/UI |
| Flor Rivas Luna | [LinkedIn](https://www.linkedin.com/in/floridesign/) - [GitHub](https://github.com/FlorRivas) - [Behance](https://www.behance.net/floridesign) | Diseño UX/UI |
| Ignacio Nicolas Basilio Buracco | [GitHub](https://github.com/NachoBasilio) - [LinkedIn](https://www.linkedin.com/in/ignacio-nicolas-basilio-buracco/) | Frontend |
| Carlos Andres Aguirre Ariza | [GitHub](https://github.com/The-Asintota) - [LinkedIn](https://www.linkedin.com/in/carlosaguirredev/) | Backend - Frontend |
