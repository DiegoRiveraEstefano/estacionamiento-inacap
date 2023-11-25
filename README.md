# estacionamiento-inacap

Uso
-----

Primero, instalar dependencias:

    $ pip install -r requirements.txt

    $ cd frontend && npm install && cd ..

Luego levantar los servicios

    $ python backend/manage.py migrage && python backend/manage.py runserver

    $ cd frontend && npm run dev


para probar el sistema se puede utilizar el siguiente script

    $ python simulator.py
