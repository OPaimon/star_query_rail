from fastapi import APIRouter

from star_query_rail.dependence.models import UserTest
from star_query_rail.utils.simnet_test import get_character_info_by_query, parse_cookie

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello World"}


@router.post("/")
async def get_characters(user_in: UserTest):
    cookie = parse_cookie(user_in.cookie)
    character_info = await get_character_info_by_query(cookie, user_in.userid)
    return character_info
