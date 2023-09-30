
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
from datetime import datetime, timedelta
import pytz

def activate_sheet(): 
    current_dir = os.getcwd()
    path = f"{current_dir}/monitoring_data.xlsx"
    if os.path.exists(path) == False:
        wb = Workbook()
        wb.save(filename="monitoring_data.xlsx")
        df_prods = pd.DataFrame (columns = ['channel_name', 'username', 'text', 'timestamp', 'tag'])
        df_prods.to_excel("monitoring_data.xlsx", index=False, sheet_name = "Monitor Data")
    else:
        pass
activate_sheet()

# get your api_id, api_hash, token
tag_list = ["pakistan", "paf","اسلام آباد", "پاکستان","pakistan air force", "pak military", "pak army","leaked database","Pakistan's military","python","machine learning","natural language processing"]
api_id = '24989393'
api_hash = 'e03b334b1cb52fc5c6a90f1837bbc184'
token = '6657308360:AAEStNbYrNu9YPueqZQquJP7TSOK8dEZJVU'
message = "Working..."
 
# your phone number
phone = '+923316007170'
  
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)


  
# connecting and building the session
# client.connect()
print("running...")
client.start(phone=phone)
print(client.get_me().stringify())
messages = client.get_messages('Shoaib Danish')

async def get_channel_name(channel_id):
    try:
        id = channel_id.chat_id
        entity = await client.get_entity(id)
        return entity.title
    except:
        return None
    
    
async def get_user_name(event):
    try:
        sender = await event.get_sender()
        last_name = sender.last_name if sender.last_name else ""
        return f"{sender.first_name} {last_name}"
    except:
        return None
    

def get_time(message_time):
    return str(message_time + timedelta(hours=5))
    

# pst = pytz.timezone('Asia/Karachi')
@client.on(events.NewMessage(incoming=True,pattern='^[a-zA-Z0-9\s_-]+$'))
async def handler(event):
    text = event.message.message if event.message.message else None
    channel_name = await get_channel_name(event.message.peer_id)
    user_name = await get_user_name(event)
    date = get_time(event.message.date)
    existance = False
    for tag in tag_list:
        if tag.lower() in event.message.message.lower():
            existance = tag
            break
    if existance:
        wb = openpyxl.load_workbook("monitoring_data.xlsx") 
        sheet = wb.active
        data = (channel_name, user_name, text, date, tag)
        sheet.append(data)
        current_dir = os.getcwd()
        path = f"{current_dir}/monitoring_data.xlsx"
        wb.save(path)
        # await event.respond('Hey!')
client.run_until_disconnected()