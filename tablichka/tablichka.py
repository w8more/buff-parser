import os
import time
import requests
import asyncio
import pandas as pd


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from parse import item_types, get_df


SPREADSHEET_ID = "1I7bKxA-XPPIhrryYJdE3KbqlASuw3aJhGmsLpp1Ja2k"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
fieldnames = ["FN", "MW", "FT", "WW", "BS"]
fieldnames = [field.lower() for field in fieldnames]

def init_table():
    creds = None
    if os.path.exists("token/token.json"):
        creds = Credentials.from_authorized_user_file("token/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("token/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheets = service.spreadsheets()
        return service, sheets
    except HttpError as err:
        print(err)
        return None, None

def get_range(what: str):
    if (what == item_types[0]): # case
        return "cases!A2:A41"
    elif (what == item_types[1]): # m9
        return "M9 Bayonet!A2:A36"

def fill_tablichka(what: str, sheets):
    if (what == item_types[0]): # case
        print("Filling google sheet with cases prices")
        df = asyncio.run(get_df(item_types[0]))
    elif (what == item_types[1]): # m9
        print("Filling google sheet with M9 prices")
        df = asyncio.run(get_df(item_types[1]))

    names = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=get_range(what)).execute().get("values")
    for row in range(len(names)):
        name = names[row][0]
        print(f"[{row}/{len(names)-1}]{name}")
        if (what == item_types[0]): # case
            buff_buy = df.loc[df.name == name].buff_buy.iloc[0]
            buff_sell = df.loc[df.name == name].buff_sell.iloc[0]
            steam_sell = df.loc[df.name == name].steam_sell.iloc[0]
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"cases!{'B'}{row+2}", valueInputOption="USER_ENTERED", body={"values": [[f"{buff_sell}"]]}).execute()
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"cases!{'C'}{row+2}", valueInputOption="USER_ENTERED", body={"values": [[f"{steam_sell}"]]}).execute()
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"cases!{'D'}{row+2}", valueInputOption="USER_ENTERED", body={"values": [[f"{buff_buy}"]]}).execute()
            time.sleep(2)
        elif (what == item_types[1]): # m9
            buff_price = []
            for field in fieldnames:
                try:
                    price = df.loc[df.name == name]["buff_" + field].iloc[0]
                    buff_price.append(price)
                except:
                    buff_price.append("nan")

            steam_price = []
            for field in fieldnames:
                try:
                    price = df.loc[df.name == name]["steam_" + field].iloc[0]
                    steam_price.append(price)
                except:
                    steam_price.append("nan")
            for i in range(5):
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"M9 Bayonet!{chr(ord('B') + i)}{row+2}", valueInputOption="USER_ENTERED", body={"values": [[f"{buff_price[i]}"]]}).execute()
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"M9 Bayonet!{chr(ord('I') + i)}{row+2}", valueInputOption="USER_ENTERED", body={"values": [[f"{steam_price[i]}"]]}).execute()
            time.sleep(10)
    
    if what == item_types[0]:
        row = 3
    if what == item_types[1]:
        row = 9
    
    df = asyncio.run(get_df("last_parsed"))
    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"status!D{row}", valueInputOption="USER_ENTERED", body={"values": [[f"{df[what][0]}"]]}).execute()

    print("Filling completed", end="\n\n")



def main():
    service, sheets = init_table()
    fill_tablichka("m9", sheets)
    # if (True):
    #     for item in item_types:
    #         fill_tablichka(item, sheets)
    #         sleep(10)
    

if __name__ == "__main__":
    main()