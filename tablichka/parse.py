import requests
import asyncio
import pandas as pd

from datetime import datetime
from database.asyn import async_session_maker
from sqlalchemy import select, text, update, insert

from database.models import Case, M9, LastParsed

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

async def parse(
    item_type: str,
):
    global qualities

    is_listening = True

    cookies = {'session': '1-cpRixN0w9CH_Mz7EmjW1h4z8Kym04lV01GJeVYe2Q5gt2033478986'}
    category = ""
    page_num = 0
    if item_type == item_types[0]:
        category = "csgo_type_weaponcase"
        page_num = 20
    elif item_type == item_types[1]:
        category = "weapon_knife_m9_bayonet"
        page_num = 11
    srcUrl = f"https://buff.163.com/api/market/goods?game=csgo&category={category}&page_num="


    async with async_session_maker() as session:
        #stmt = text(f"DELETE FROM \"{item_type}\"")
        #await session.execute(stmt)
        for page in range(1, page_num):
            url = srcUrl + str(page)
            r = requests.get(url,cookies=cookies)    
            json_response = r.json()
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

async def get_df(table_name):
    async with async_session_maker() as session:
        query = select("*").select_from(text('"' + table_name + '"'))
        records = await session.execute(query)
        columns = records.keys()
        # Convert records to a list of dictionaries
        data = [dict(zip(columns, row)) for row in records]

        # Create a DataFrame from the data
        return pd.DataFrame(data)


async def main():
    for item in item_types:
        await parse(item)

if __name__ == "__main__":
    asyncio.run(main())