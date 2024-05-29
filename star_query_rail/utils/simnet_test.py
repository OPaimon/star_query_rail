import asyncio
from typing import Any, Dict

from arkowrapper import ArkoWrapper
from simnet import Region, StarRailClient
from simnet.models.starrail.chronicle.characters import StarRailDetailCharacter


def parse_cookie(text: str) -> Dict[str, Any]:
    """解析 Cookie 字符串"""
    try:
        # cookie str to dict
        wrapped = (
            ArkoWrapper(text.split(";"))
            .filter(lambda x: x != "")
            .map(lambda x: x.strip())
            .map(lambda x: ((y := x.split("=", 1))[0], y[1]))
        )
        cookie = dict(wrapped)
    except (AttributeError, ValueError, IndexError):
        return {}
    return cookie


def print_character_info(character: StarRailDetailCharacter):
    """以高可读性打印 StarRailDetailCharacter 的内容"""

    print(f"角色信息：{character.name}")
    print(f"  ID: {character.id}")
    print(f"  元素: {character.element}")
    print(f"  稀有度: {character.rarity} 星")
    print(f"  等级: {character.level}")
    print(f"  突破等级: {character.rank}")
    print(f"  装备: {character.equip.name if character.equip else '无'}")

    print("\n遗物:")
    for relic in character.relics:
        print(f"  {relic.name}")
        print(f"    等级: {relic.level}")
        tmp: str = f"    主属性: {relic.main_property.property_type}"
        tmp += f" - {relic.main_property.times}"
        tmp += f" - {relic.main_property.value}"
        print(tmp)
        for prop in relic.properties:
            print(f"    副属性: {prop.property_type} - {prop.times} - {prop.value}")

    print("\n属性:")
    for prop in character.properties:
        print(f"  {prop.property_type}: {prop.final}")

    print("\n技能:")
    for skill in character.skills:
        print(f"  {skill.point_id} - {skill.point_type}")
        print(f"    等级: {skill.level}")
        print(f"    激活: {skill.is_activated}")
        print(f"    受突破影响: {skill.is_rank_work}")
        for stage in skill.skill_stages:
            print(f"      阶段: {stage.level} - {stage.name} - {stage.desc}")

    print(f"\n基础类型: {character.base_type}")
    print(f"模型路径: {character.figure_path}")


async def print_character_info_by_query(cookies: Dict[str, Any], player_id: int):
    print("Test")
    async with StarRailClient(
        cookies,
        player_id=player_id,
        region=Region.CHINESE,
        device_id=cookies.get("x-rpc-device_id"),
        device_fp=cookies.get("x-rpc-device_fp"),
    ) as client:
        # data = await client.get_character_details(1305)
        # # 遍历角色基本信息
        # print(f"角色 ID: {data.avatar.id}")
        # print(f"角色名称: {data.avatar.name}")
        # print(f"角色元素: {data.avatar.element.value}")
        # print(f"角色命途: {data.avatar.path.value}")
        # print(f"角色当前等级: {data.avatar.cur_level}")

        # # 遍历武器信息
        # if data.equipment:
        #     print(f"武器 ID: {data.equipment.id}")
        #     print(f"武器名称: {data.equipment.name}")
        #     print(f"武器稀有度: {data.equipment.rarity}")
        #     print(f"武器命途: {data.equipment.path.value}")
        #     print(f"武器当前等级: {data.equipment.cur_level}")

        # # 遍历天赋信息
        # print("天赋信息:")
        # for skill in data.skills:
        #     print(f"  - 天赋 ID: {skill.id}")
        #     print(f"  - 天赋名称: {skill.anchor}")
        #     print(f"  - 天赋当前等级: {skill.cur_level}")
        #     print(f"  - 天赋进度: {skill.progress}")

        # # 遍历其他技能信息
        # print("其他技能信息:")
        # for skill in data.skills_other:
        #     print(f"  - 技能 ID: {skill.id}")
        #     print(f"  - 技能名称: {skill.anchor}")
        #     print(f"  - 技能当前等级: {skill.cur_level}")
        #     print(f"  - 技能进度: {skill.progress}")
        data = await client.get_starrail_characters()
        # 遍历角色列表
        print("角色列表:")
        for character in data.avatar_list:
            print_character_info(character)
