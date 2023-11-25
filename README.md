# estacionamiento-inacap

Descripcion
-----
Esta aplicacion es una prueba conceptual sobre un sistema de estacionamiento.
donde se intenta automatizar los sitemas de pago y salida/entrada de vehiculos.

la aplicacion usa las tegnologias de:
 - python junto a django y django-rest-framework
 - nodejs utilizando astro con vuejs y bulma css para los estilos

Uso
-----

Primero, instalar dependencias:

    $ pip install -r requirements.txt

    $ cd frontend && npm install && cd ..


Tambien es necesario crear un archivo .env donde colocar las siguientes variables de entorno:

 - PAYPAL_CLIENT_ID
 - PAYPAL_CLIENT_SECRET

estas se optiene desde el portal de developers de paypal

Luego levantar los servicios

    $ python backend/manage.py migrage && python backend/manage.py runserver

    $ cd frontend && npm run dev


para probar el sistema se puede utilizar el siguiente script

    $ python simulator.py
