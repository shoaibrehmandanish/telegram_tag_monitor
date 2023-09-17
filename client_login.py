
# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import openpyxl
import pandas as pd
from openpyxl import Workbook
import os
import re
 
def activate_sheet(): 
    current_dir = os.getcwd()
    path = f"{current_dir}/products.xlsx"
    if os.path.exists(path) == False:
        wb = Workbook()
        wb.save(filename="products.xlsx")
        df_prods = pd.DataFrame (columns = ['channel_id', 'user_id', 'text', 'timestamp'])
        df_prods.to_excel("products.xlsx", index=False, sheet_name = "Products Data")
    else:
        pass
activate_sheet()

# get your api_id, api_hash, token
tag_list = ["pakistan", "paf", "islamabad", "asia cup", "asia cup final","Premium Account","python","machine learning","natural language processing"]
api_id = '24989393'
api_hash = 'e03b334b1cb52fc5c6a90f1837bbc184'
token = '6533090846:AAEG9DUTXAOPhLGMjx6FCfbvXwlq4nZyylw'
message = "Working..."
 
# your phone number
phone = '+923316007170'
  
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

  
# connecting and building the session
client.connect()
print("running...")
# client.start()
# print(client.get_me().stringify())
# client.send_message('Shoaib Danish', 'Hello! Talking to you from Telethon')

def get_channel_id(channel_id):
    try:
        return channel_id.chat_id
    except:
        return None


@client.on(events.NewMessage(pattern='^.{1,50000}$'))
async def handler(event):
    text = event.message.message if event.message.message else None
    channel_id = get_channel_id(event.message.peer_id)
    user_id = event.message.from_id.user_id if event.message.from_id else None
    date = str(event.message.date)
    existance = False
    print(tag_list)
    for tag in tag_list:
        if tag.lower() in event.message.message.lower():
            existance = True
    if existance:
        wb = openpyxl.load_workbook("products.xlsx") 
        sheet = wb.active
        data = (channel_id, user_id, text, date)
        sheet.append(data)
        current_dir = os.getcwd()
        path = f"{current_dir}/products.xlsx"
        wb.save(path)
        print("save")
        # await event.respond('Hey!')
client.run_until_disconnected()
