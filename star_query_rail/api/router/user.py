from fastapi import APIRouter, HTTPException
from simnet import Region, StarRailClient
from simnet.errors import TimedOut
from simnet.models.starrail.chronicle.characters import StarRailDetailCharacters

from star_query_rail.api.dep import CurrentAccount, SessionDep
from star_query_rail.dependence import crud
from star_query_rail.dependence.models import (
    Character,
    CharacterRegister,
    CharacterUpdate,
    ConnectEU,
    ConnectEUPublic,
    ConnectEURegister,
    ConnectUCRegister,
    EUCPublic,
    Message,
    Userbase,
    UserCreate,
    Userinfo,
    UserRegister,
)
from star_query_rail.utils.parse import parse_cookie

router = APIRouter()


@router.post("/", response_model=EUCPublic)
async def bind_user(
    session: SessionDep, current_account: CurrentAccount, user_in: UserCreate
) -> EUCPublic:
    """
    Bind user to account
    """
    cookies = parse_cookie(user_in.cookie)
    async with StarRailClient(
        cookies,
        region=Region.CHINESE,
        device_id=cookies.get("x-rpc-device_id"),
        device_fp=cookies.get("x-rpc-device_fp"),
        lang="zh-cn",
    ) as client:
        account_id = client.account_id
        data = await client.get_starrail_accounts()
        user_out = data.pop()
        nickname = user_out.nickname
        data.append(user_out)
    created_user = session.get(Userinfo, account_id)
    if not created_user:
        created_user = crud.create_user(
            session=session,
            user_create=UserRegister(
                userid=account_id, nickname=nickname, cookies=cookies
            ),
        )
    user = Userbase.model_validate(created_user)
    created_eu = session.get(
        ConnectEU, {"userid": created_user.userid, "email": current_account.email}
    )
    if created_eu:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    if not created_eu:
        created_eu = crud.create_eu(
            session=session,
            eu_connect=ConnectEURegister(
                userid=created_user.userid, email=current_account.email
            ),
        )
    eu = ConnectEUPublic(
        userid=created_eu.userid, email=created_eu.email, nickname=user.nickname
    )
    characters = list()
    for ele in data:
        cur_character = session.get(Character, ele.uid)
        if not cur_character:
            crud.create_character(
                session=session,
                character_create=CharacterRegister(cid=ele.uid, name=ele.nickname),
            )
        character = CharacterRegister(cid=ele.uid, name=ele.nickname)
        characters.append(character)
    euc = EUCPublic(
        email=eu.email, userid=eu.userid, nickname=eu.nickname, characters=characters
    )
    return euc


@router.post("/get")
async def get_characters_detail(
    session: SessionDep, current_account: CurrentAccount, cnt_uc: ConnectUCRegister
) -> StarRailDetailCharacters:
    """
    Get characters info
    """
    if not session.get(
        ConnectEU, {"userid": cnt_uc.userid, "email": current_account.email}
    ):  # noqa: E501
        raise HTTPException(
            status_code=400,
            detail="the account is not bind to the user.",
        )
    cnt_cookies = session.get(Userinfo, cnt_uc.userid).cookies
    characters_detail = session.get(Character, cnt_uc.cid).data
    try:
        async with StarRailClient(
            cnt_cookies,
            player_id=cnt_uc.cid,
            region=Region.CHINESE,
            device_id=cnt_cookies.get("x-rpc-device_id"),
            device_fp=cnt_cookies.get("x-rpc-device_fp"),
            lang="zh-cn",
        ) as client:
            data = await client.get_starrail_characters()
            crud.update_character(
                session=session,
                character_update=CharacterUpdate(cid=cnt_uc.cid, data=data.dict()),
            )
        return data
    except TimedOut:
        return characters_detail


@router.get("/get-info", response_model=EUCPublic)
async def get_info(session: SessionDep, current_account: CurrentAccount) -> EUCPublic:
    """
    Get user info
    """
    euc_public = EUCPublic(email=current_account.email)
    connect_eu = session.query(ConnectEU).filter_by(email=current_account.email).first()
    if connect_eu:
        euc_public.userid = connect_eu.userid
    else:
        return euc_public
    cookies = session.get(Userinfo, euc_public.userid).cookies
    async with StarRailClient(
        cookies,
        region=Region.CHINESE,
        device_id=cookies.get("x-rpc-device_id"),
        device_fp=cookies.get("x-rpc-device_fp"),
        lang="zh-cn",
    ) as client:
        account_id = client.account_id
        data = await client.get_starrail_accounts()
        user_out = data.pop()
        nickname = user_out.nickname
        data.append(user_out)
    euc_public.nickname = nickname
    characters = list()
    for ele in data:
        cur_character = session.get(Character, ele.uid)
        if not cur_character:
            crud.create_character(
                session=session,
                character_create=CharacterRegister(cid=ele.uid, name=ele.nickname),
            )
        character = CharacterRegister(cid=ele.uid, name=ele.nickname)
        characters.append(character)
    euc_public.characters = characters
    return euc_public


@router.delete("/unbind/{userid}", response_model=Message)
def unbind_user(
    session: SessionDep, current_account: CurrentAccount, userid: int
) -> Message:
    """
    Unbind user from account
    """
    bind = session.get(ConnectEU, {"userid": userid, "email": current_account.email})
    if not bind:
        raise HTTPException(
            status_code=400,
            detail="The user with this email does not exist in the system.",
        )
    session.query(ConnectEU).filter_by(
        userid=userid, email=current_account.email
    ).delete()
    session.commit()
    return Message(message="Account unbinded")


@router.delete("/delcharacter/{cid}", response_model=Message)
def delete_character(
    session: SessionDep, current_account: CurrentAccount, cid: int
) -> Message:
    """
    Delete character
    """
    if not current_account.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="You do not have the permission to delete characters.",
        )
    character = session.get(Character, cid)
    if not character:
        raise HTTPException(
            status_code=400,
            detail="The character does not exist in the system.",
        )
    session.query(Character).filter_by(cid=cid).delete()
    session.commit()
    return Message(message="Character deleted")
