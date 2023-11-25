# estacionamiento-inacap

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
