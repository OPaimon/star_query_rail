from fastapi import APIRouter

import star_query_rail.api.router.example as example
import star_query_rail.api.router.login as login
import star_query_rail.api.router.user as user

api_router = APIRouter()
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
