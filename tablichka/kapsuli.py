import time
import requests
import asyncio

from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

from sqlalchemy import select, text, update, insert, Column, Integer, text
from database.asyn import async_session_maker, engine
from database.models import Capsule_quantites

from parse import get_df

capsule_urls = [
"https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&category_730_Weapon%5B%5D=any&category_730_Tournament%5B%5D=tag_Tournament21&appid=730&q=capsule",
"https://steamcommunity.com/market/search?q=capsule&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&category_730_Weapon%5B%5D=any&category_730_Tournament%5B%5D=tag_Tournament19&appid=730",
"https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Type%5B0%5D=tag_CSGO_Type_WeaponCase&category_730_Weapon%5B0%5D=any&category_730_Tournament%5B0%5D=tag_Tournament17&appid=730",
]

sticker_urls = [
    "https://steamcommunity.com/market/search?appid=730&q=9INE+%7C+Paris+2023",
]

async def do_something(items):
    async with async_session_maker() as session:
        now = datetime.now().date()
        existing_item = await session.execute(select(Capsule_quantites).filter(Capsule_quantites.date == now))
        existing_item = existing_item.scalar_one_or_none()

        if existing_item is None:
            stmt = insert(Capsule_quantites).values(items)
        else:
            stmt = update(Capsule_quantites).where(Capsule_quantites.date == now).values(items)
        await session.execute(stmt)
        await session.commit()

def parse_for_sticker_quantities():
    sticker = {}
    sticker["date"] = datetime.now().date()
    for url in sticker_urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            name_elements = soup.find_all("span", class_="market_listing_item_name")
            
            quantity_elements = soup.find_all("span", class_="market_listing_num_listings_qty")

            min_length = min(len(name_elements), len(quantity_elements))
            
            for name_element, quantity_element in zip(name_elements[:min_length], quantity_elements[:min_length]):
                raw_name = name_element.text.strip()
                name = raw_name.replace(" ", "_")
                name = ''.join(e for e in name if e.isalnum() or e == '_')
                name = name.lower()
                if name == "sticker__9ine__paris_2023":
                    quantity = int(quantity_element.get("data-qty"))
                    sticker[name] = quantity
                # capsule[name] = quantity
        else:
            print("Failed to retrieve page:", response.status_code)
    return sticker

def parse_for_capsule_quantities():
    capsule = {}
    capsule["date"] = datetime.now().date()
    for url in capsule_urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            name_elements = soup.find_all("span", class_="market_listing_item_name")
            
            quantity_elements = soup.find_all("span", class_="market_listing_num_listings_qty")

            min_length = min(len(name_elements), len(quantity_elements))
            
            for name_element, quantity_element in zip(name_elements[:min_length], quantity_elements[:min_length]):
                raw_name = name_element.text.strip()
                name = raw_name.replace(" ", "_")
                name = ''.join(e for e in name if e.isalnum() or e == '_')
                name = name.lower().replace("2020_rmr", "rmr_2020")
                quantity = int(quantity_element.get("data-qty"))
                capsule[name] = quantity
        else:
            print("Failed to retrieve page:", response.status_code)
    return capsule

async def need_to_update():
    async with async_session_maker() as session:
        now = datetime.now().date()
        existing_item = await session.execute(select(Capsule_quantites).filter(Capsule_quantites.date == now))
        existing_item = existing_item.scalar_one_or_none()

        if existing_item is None:
            return True
        else: 
            return False

def main():
    if asyncio.run(need_to_update()):
        print("updating")
        a = True
        b = True
        capsule = None
        sticker = None
        
        while a or b:
            if a:
                print("parsing capsules")
                capsule = parse_for_capsule_quantities()
                if len(capsule.values()) == 18:
                    a = False
                

            if b:
                print("parsing stickers")
                sticker = parse_for_sticker_quantities()
                if len(sticker.values()) == 2:
                    b = False

            time.sleep(5)
            
        asyncio.run(do_something(capsule))
        asyncio.run(do_something(sticker))
    else:
        print("nothing to update")
        time.sleep(1)






if __name__ == "__main__":
    main()

