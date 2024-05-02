# 1. Contribuyendo a nuestro proyecto

¡Saludos y bienvenidos a nuestro proyecto! Estamos encantados con su interés en contribuir. Este documento sirve como una guía completa, brindándole información sobre cómo configurar su entorno de desarrollo y describiendo las pautas a seguir al modificar archivos o realizar contribuciones.

## 1.1. Estándares de codificación

Para el desarrollo de este proyecto, utilizamos la biblioteca [black](https://black.readthedocs.io/en/stable/) para formatear el código de acuerdo con [PEP8](https://peps.python.org/pep-0008/) un estándar de estilo de código para Python. Además, utilizamos [pre-commit](https://pre-commit.com/) para administrar hooks de Git personalizados. Estas herramientas nos ayudan a mantener un estilo de código coherente en todos los archivos Python del proyecto y a mantener el historial de commits en línea con el estándar [ConventionalCommits](https://www.conventionalcommits.org/en/v1.0.0/). Estas bibliotecas ya están configuradas en el proyecto, sin embargo, para que funcionen correctamente se deben realizar los siguientes pasos:

- **Paso 1 (Instalación de los hooks):** Un hook de Git es un script que Git ejecuta antes o después de eventos como **commit**, **push** o **merge**. Estos enlaces se utilizan para automatizar tareas en el flujo de trabajo de desarrollo, como aplicar un formato de mensaje de confirmación, ejecutar pruebas antes de realizar una confirmación o incluso verificar el estilo del código. Este proyecto incluye dos hooks personalizados que garantizan que el código tenga el formato correcto y que el mensaje de confirmación cumpla con el estándar **ConventionalCommits**, para inicializar estas validaciones dedbes ejecutar los siguientes comandos.

    ```bash
    pre-commit install
    pre-commit install --hook-type commit-msg
    ```

## 1.2. Directrices para los commits

Usamos la biblioteca [commitizen](https://commitizen-tools.github.io/commitizen/) para gestionar mensajes de confirmación, esta biblioteca simplifica el proceso de realizar un commit a través de una interfaz de terminal donde mediante pasos se irá construyendo el mensaje  del commit siguiendo el estándar **ConventionalCommits**.

### 1.2.1. Casos de uso

- **Commit realizado correctamente:** Para realizar un commit con éxito, el código debe tener el formato correcto. Gracias a esta biblioteca, podemos asegurarnos de que nuestro mensaje  para el commit se adhiera al estándar seleccionado dentro del proyecto.

<div>
    <img src="https://commitizen-tools.github.io/commitizen/images/demo.gif">
</div>

- **Realización del commit fallida:** Cuando se intenta ejecutar una confirmación y el código no está formateado correctamente, el proceso de confirmación se cancelará. La consola mostrará los archivos que necesitan formato y las áreas específicas dentro de cada archivo que no se adhieren al formato de código establecido. No se realizará un commit con éxito hasta que sé de el formato correcto a los archivos que lo requieren.

<div>
    <img src="/images/CommitizenExanple1.png">
</div>

Al existir un fichero con un formato incorrecto puede usar la biblioteca **black** para dar formato al codigo de manera automatica con el siguiente commando.

```bash
black src/
```

Luego agrega las modificaciones al aerea de confirmación de Git y podra realizar con exito el commit anterior.

# 2. Principios de la Comunidad

Por favor sea respetuoso y considerado con los demás. Seguimos el [Código de conducta del Pacto del colaborador](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).