from fastapi import APIRouter

import star_query_rail.api.router.example as example

api_router = APIRouter()
api_router.include_router(example.router, prefix="/example", tags=["example"])
