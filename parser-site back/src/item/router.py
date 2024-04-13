import requests
from datetime import datetime
import asyncio

import pandas as pd
from fastapi import APIRouter, Depends, WebSocket

from sqlalchemy import insert, select, Table, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session, async_session_maker, Base, engine
from src.item.models import Case, M9, LastParsed

from src.config import settings
from src.http_client import BuffHTTPClient

buff_client = BuffHTTPClient(
    base_url="https://buff.163.com",
    cookies={"session": settings.COOKIES}
)

router = APIRouter(
    prefix = "/item",
    tags = ["Item"]
)

item_types = [
    "case",
    "m9",
]

qualities = {
    "(Factory New)": "FN",
    "(Minimal Wear)": "MW",
    "(Well-Worn)": "WW",
    "(Field-Tested)": "FT",
    "(Battle-Scarred)": "BS",
}

is_listening = False
completed = 0

@router.websocket("/get_completed")
async def get_completed(websocket: WebSocket):
    global is_listening
    await websocket.accept()
    last_message = ""
    while True:
        if (last_message != completed):
            if is_listening:
                if completed == 100:
                    await websocket.send_text("completed")
                else:
                    await websocket.send_text(str(completed))
                last_message = completed
                
            else:
                await websocket.send_text("parse")
                last_message = completed
        await asyncio.sleep(1)

@router.post("/create_table")
async def create_table(session: AsyncSession = Depends(get_async_session)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "OK"}

@router.post("/parse/{item_type}")
async def parse_item(item_type: str):
    global completed
    completed = 0
    asyncio.create_task(parse(item_type))
    return {"parsing started"}

@router.get("/get_all_item_types")
async def get_all_item_types():
    return item_types

@router.get("/get_items/{item_type}")
async def get_item(item_type: str):
    if (item_type in item_types):
        result = await get_df(item_type)
        result = result.to_json()
        return result
    else:
        return None

@router.get("/get_item/{item_type}/{id}")
async def get_item(item_type: str, id: int):
    if (item_type in item_types):
        result = await get_df(item_type)
        return result.iloc[id].to_json()
    else:
        return None

async def get_df(table_name: str):
    async with async_session_maker() as session:
        query = select("*").select_from(text('"' + table_name + '"'))
        records = await session.execute(query)
        columns = records.keys()
        # Convert records to a list of dictionaries
        data = [dict(zip(columns, row)) for row in records]

        for row in data:
            for key, value in row.items():
                if isinstance(value, float) and pd.isna(value):
                    row[key] = None

        # Create a DataFrame from the data
        return pd.DataFrame(data)

async def parse(item_type: str):
    global is_listening
    global completed
    global qualities

    is_listening = True

    cookies = {'session': settings.COOKIES}
    category = ""
    page_num = 0
    if item_type == item_types[0]:
        category = "csgo_type_weaponcase"
        page_num = 20
    elif item_type == item_types[1]:
        category = "weapon_knife_m9_bayonet"
        page_num = 11


    async with async_session_maker() as session:
        stmt = text(f"DELETE FROM \"{item_type}\"")
        await session.execute(stmt)
        for page in range(1, page_num):
            json_response = await buff_client.parse_page(page_num=page, category=category)
            items = json_response["data"]["items"]
            for item in items:
                name = item["name"]
                buff_sell_price = float(item["sell_min_price"])
                buff_buy_price = float(item["buy_max_price"])
                steam_sell_price = float(item["goods_info"]["steam_price_cny"])

                if item_type == item_types[0]:
                    existing_case = await session.execute(select(Case).filter(Case.name == name))
                    existing_case = existing_case.scalar_one_or_none()
                    if existing_case is None:
                        stmt = insert(Case).values({"name": name, "buff_buy": buff_buy_price, "buff_sell": buff_sell_price,"steam_sell": steam_sell_price})
                    else:
                        stmt = update(Case).where(Case.name == name).values({"buff_buy": buff_buy_price, "buff_sell": buff_sell_price,"steam_sell": steam_sell_price})
                    await session.execute(stmt)
                elif item_type == item_types[1]:
                    try:
                        hash_name = item['market_hash_name']
                        index = hash_name.index("(")
                        name = hash_name[:index-1]
                        quality = hash_name[index:]
                        quality = qualities[quality]
                    except:
                        quality = "FN"

                    existing_m9 = await session.execute(select(M9).filter(M9.name == name))
                    existing_m9 = existing_m9.scalar_one_or_none()

                    if existing_m9 is None:
                        stmt = insert(M9).values({"name": name, "buff_" + quality.lower(): buff_sell_price, "steam_" + quality.lower(): steam_sell_price})
                    else:
                        stmt = update(M9).where(M9.name == name).values({"buff_" + quality.lower(): buff_sell_price, "steam_" + quality.lower(): steam_sell_price})
                    await session.execute(stmt)


            print(f"page {page}/{page_num-1}")
            completed = round(page / (page_num-1) * 100)
            await asyncio.sleep(5)
        existing_id = await session.execute(select(LastParsed).filter(LastParsed.id == 0))
        existing_id = existing_id.scalar_one_or_none()
        if existing_id == None:
            stmt = insert(LastParsed).values({"id": 0, item_type: datetime.now()})
        else:
            stmt = update(LastParsed).where(LastParsed.id == 0).values({item_type: datetime.now()})
        await session.execute(stmt)
        await session.commit()
    is_listening=False