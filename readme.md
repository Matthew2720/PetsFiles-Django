# PetsFiles-Django

## Descripción
"PetsFiles-Django" es una aplicación web robusta y completa para la gestión de información relacionada con mascotas. Esta solución integral está diseñada para facilitar la administración de datos vitales asociados con mascotas, médicos veterinarios y clientes. Entre sus funcionalidades clave se incluyen el registro detallado de mascotas, la gestión de citas veterinarias, el seguimiento de historiales médicos, la administración de un calendario de eventos y recordatorios, y la gestión de medicamentos. 

La aplicación está construida con el framework Django, aprovechando su poderosa infraestructura para ofrecer un sitio web seguro, eficiente y fácil de mantener. Además, se incluye un manual de usuario (`manual_usuario.pdf`) que ofrece instrucciones claras sobre cómo utilizar la aplicación, asegurando una experiencia de usuario fluida y accesible.

## Tecnologías Utilizadas

- **Django**: Framework web principal utilizado para el desarrollo del proyecto, proporcionando una estructura de proyecto completa que incluye manejo de usuarios, plantillas, rutas (URLs), y modelos de datos.
- **Python**: Lenguaje de programación principal utilizado en el proyecto, aprovechando la versatilidad y la amplia biblioteca de recursos de Python.
- **SQLite**: Sistema de gestión de bases de datos utilizado para el desarrollo local, ofreciendo una solución de almacenamiento de bases de datos simple y eficiente.
- **HTML, CSS, y JavaScript**: Tecnologías utilizadas para el desarrollo del frontend, permitiendo crear una interfaz de usuario atractiva y funcional.

## Dependencias

- **Autenticación y Autorización**: Utilización de módulos como `django-allauth` para facilitar la autenticación de usuarios, incluyendo el registro, el inicio de sesión y la gestión de cuentas.
- **Manejo de Imágenes**: Implementación de `Pillow` para el procesamiento de imágenes en Django, esencial para la gestión de fotografías de mascotas.
- **Calendario y Eventos**: Uso de `django-calendarium` para la gestión de eventos y calendarios, permitiendo a los usuarios mantener un seguimiento eficiente de citas y recordatorios.

Para conocer las dependencias específicas y sus versiones, se incluye el archivo `requirements.txt` en el proyecto, facilitando la instalación y configuración del entorno necesario para ejecutar la aplicación.

## Cómo Empezar

Para configurar y ejecutar "PetsFiles-Django" en su entorno local, siga los pasos detallados a continuación:

1. Clone el repositorio en su máquina local.
2. Instale las dependencias necesarias utilizando el comando `pip install -r requirements.txt`.
3. Realice las migraciones necesarias con `python manage.py migrate` para preparar la base de datos.
4. Inicie el servidor de desarrollo con `python manage.py runserver`.
5. Acceda a la aplicación a través de su navegador web en `http://127.0.0.1:8000/`.

Para más detalles sobre el uso y la configuración de la aplicación, refiérase al `manual_usuario.pdf` incluido en el repositorio.
