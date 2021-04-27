# cassandra-fastapi

A example of microservicemade with `FastAPI <https://github.com/tiangolo/fastapi>`_ (0.63+) for Apache Cassandra (3.0+) and `DataStax python-driver <https://github.com/datastax/python-driver>`_ secured with API keys check.

The driver supports Python 3.7 and 3.8+.


Installation
------------
Fist you must git clone this repository:

    $ git clone https://github.com/Rekoc/cassandra-fastapi.git

Then installation through pip and virtual-env is recommended:

    $ cd cassandra-fastapi
    $ pip install -r requirements.txt
    
You must have installed Apache Cassandra (3.0+) on your cloud/desktop.
Finally, lunch the FastAPI app:

    $ uvicorn main:app --reload
    
All good !
