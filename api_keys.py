from fastapi import Security
from fastapi import HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader

from starlette import status

from dotenv import load_dotenv

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
# Load the env variables in .env
load_dotenv(os.path.join(PROJECT_DIR, '.env'))

# API keys
LIST_API_KEY = os.getenv('LIST_API_KEY').split(' ')
API_KEY_NAME = os.getenv('API_KEY_NAME')
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN')

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_query: str = Security(api_key_query),
                      api_key_header: str = Security(api_key_header),
                      api_key_cookie: str = Security(api_key_cookie)):
    if api_key_query in LIST_API_KEY:
        return api_key_query
    elif api_key_header in LIST_API_KEY:
        return api_key_header
    elif api_key_cookie in LIST_API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )