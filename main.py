from typing import Optional

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
session = cluster.connect('data')
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
    rows = session.execute("SELECT * FROM {}".format(table))
    data = {}
    for row in rows:
        data[row.id] = row.value
    return JSONResponse(
        data,
        status_code=status.HTTP_200_OK
    )

@app.post("/model/{table}")
def post_model(table: str, item: MyModel):
    """
    Add a new model in the table
    """
    returned_value = session.execute(
        "INSERT INTO {} (id, value) VALUES ({}, {})".format(table, item.id, item.value)
    )
    return JSONResponse(
        {'detail': "model has been added"},
        status_code=status.HTTP_200_OK
    )