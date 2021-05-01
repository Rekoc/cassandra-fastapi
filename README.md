# cassandra-fastapi

A example of microservicemade with [FastAPI](https://github.com/tiangolo/fastapi) (0.63+) for Apache Cassandra (3.0+) and [DataStax python-driver](https://github.com/datastax/python-driver) secured with API keys check.

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

Requests
-----------
Check http://127.0.0.1:8000/docs in your web browser.

How-to adapt the code ?
------------
1. Create your own model(s) in models.exemple, check https://fastapi.tiangolo.com/ for more informations
2. Update the request's model
```python
@app.post("/model/{table}")
async def post_model(table: str, item: MyModel,
                     api_key: APIKey = Depends(get_api_key)):
    returned_value = session.execute(
        "INSERT INTO {} (id, value) VALUES ({}, {});".format(table, item.id, item.value)
    )
    return JSONResponse(
        {'detail': "model has been added"},
        status_code=status.HTTP_200_OK
    )
```
becomes
```python
@app.post("/model/{table}")
async def post_model(table: str, item: MyOwnModelMadeForMyApp,
                     api_key: APIKey = Depends(get_api_key)):
    returned_value = session.execute(
        "INSERT INTO {} (field_id, field_value, new_field) VALUES ({}, {}, {});".format(table, item.field_id, item.field_value, item.new_field, ...)
    )
    return JSONResponse(
        {'detail': "model has been added"},
        status_code=status.HTTP_200_OK
    )
```

