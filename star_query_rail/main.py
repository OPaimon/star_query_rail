# type: ignore[attr-defined]
import fastapi
from fastapi import APIRouter
from rich import pretty

from star_query_rail import version
from star_query_rail.api import api_router

app = fastapi.FastAPI(
    title="star_query_rail",
    description="A tool for query some infomation about a game",
    version=version,
)

pretty.install()


app.include_router(api_router)
