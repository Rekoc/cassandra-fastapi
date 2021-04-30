from typing import Optional, List

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKey

from starlette import status
from starlette.responses import RedirectResponse, JSONResponse

from models.exemple import MyModel
from api_keys import get_api_key

from cassandra.cluster import Cluster

# Cassandra init
# 127.0.0.1
cluster = Cluster()
session = cluster.connect('data') # 'data' is the database name
# session.set_keyspace('users')

app = FastAPI()
# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.get("/health")
async def health():
    """
    Make sur your API is running
    """
    return JSONResponse(
        {"detail": "All good!"},
        status_code=status.HTTP_200_OK
    )

@app.get("/health-secure")
async def health_secured(api_key: APIKey = Depends(get_api_key)):
    """
    Make sure your API credentials are valid and run
    """
    return JSONResponse(
        {"detail": "All good!"},
        status_code=status.HTTP_200_OK
    )

@app.get("/models/{table}")
async def get_models(table: str,
                     api_key: APIKey = Depends(get_api_key)):
    """
    Return all models
    """
    rows = session.execute("SELECT * FROM {};".format(table))
    data = {'items': {}}
    for row in rows:
        data['items'][row.id] = row.value
    data['count'] = len(data['items'])
    return JSONResponse(
        data,
        status_code=status.HTTP_200_OK
    )

@app.post("/model/{table}")
async def post_model(table: str, item: MyModel,
               api_key: APIKey = Depends(get_api_key)):
    """
    Add a new model in the table
    """
    returned_value = session.execute(
        "INSERT INTO {} (id, value) VALUES ({}, {});".format(table, item.id, item.value)
    )
    return JSONResponse(
        {'detail': "model has been added"},
        status_code=status.HTTP_200_OK
    )

@app.put("/model/{table}")
async def put_model(table: str, item: MyModel,
              api_key: APIKey = Depends(get_api_key)):
    """
    Update model in the table
    """
    returned_value = session.execute(
        """
        UPDATE {}
        SET value = {}
        WHERE id = {};
        """.format(table, item.value, item.id)
    )
    return JSONResponse(
        {'detail': "model has been updated"},
        status_code=status.HTTP_200_OK
    )

# /model/{table}?id=xxxxxxxxxx
@app.delete("/model/{table}")
async def delete_model(table: str, id: str,
                 api_key: APIKey = Depends(get_api_key)):
    """
    Delete model from the table
    """
    returned_value = session.execute(
        """
        DELETE FROM {} WHERE id = {};
        """.format(table, id)
    )
    # can be --> WHERE id IN (xxxxxxxxxxxxxxx, xxxxxxxxxxxxxxx);
    return JSONResponse(
        {'detail': "model has been deleted"},
        status_code=status.HTTP_200_OK
    )

def generate_insert_cql(table: str, item: MyModel):
    return "INSERT INTO {} (id, value) VALUES ({}, {});\n".format(table, item.id, item.value)

@app.post("/models/{table}")
async def batch_post_model(table: str, items: List[MyModel],
                     api_key: APIKey = Depends(get_api_key)):
    """
    Add many new models in the table
    """
    cmd = ""
    for item in items:
        cmd += generate_insert_cql(table, item)
    returned_value = session.execute(
        """
        BEGIN BATCH
            {}
        APPLY BATCH;
        """.format(cmd)
    )
    return JSONResponse(
        {'detail': "models have been added"},
        status_code=status.HTTP_200_OK
    )