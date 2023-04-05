import discord
import requests
import os
import json
from discord.ext import commands
import asyncio
from EdgeGPT import Chatbot, ConversationStyle
intents = discord.Intents.all()
#Colors for console Output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
##

#Create Config File if needed
if not 'Config.txt' in os.listdir():
    open('Config.txt', 'w').write('{"auth_token":"","bot_token":"","channel_id":""}')
    print(bcolors.WARNING + "Warning: Config has been created. Restart The bot after filling info" + bcolors.ENDC)
if not 'Cookie.txt' in os.listdir():
    open('Config.txt', 'w').write('')
    print(bcolors.WARNING + "Warning: Cookie File has been created. Restart The bot after filling info" + bcolors.ENDC)
##

#Read Config and write to variables
ConfigFile = json.loads(open("Config.txt", "r").read())
DiscordToken = ConfigFile['bot_token']
ChannelID = ConfigFile['channel_id']
client = discord.Client(intents = intents)
channel = client.get_channel(ChannelID)
bot1 = commands.Bot(command_prefix='.', intents = intents)
messages =  []
##

#When Bot is logged in 
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="BingGPT"))
    print('Logged in as ' + client.user.name + ChannelID )
##

#Check for Messages
@client.event
async def on_message(message):
    if message.channel.id in [int(ChannelID)]:
        if message.author.id != client.user.id: 
##Send the Message to the BingChat API
            channel = client.get_channel(int(ChannelID))
            async for message in channel.history(limit=1):  
                messagevar = message.content
            print(bcolors.WARNING + "Processing: " + messagevar)
            with open('cookie.txt', 'r') as f:
                cookies = json.load(f)
            bot = Chatbot(cookies = cookies)
            response = await bot.ask(prompt=messagevar, conversation_style=ConversationStyle.creative)
            item = response.get('item')
            msgs = item.get('messages')
            list1 = [msgs[1]]
            jsonStr = json.dumps(list1)
            data = json.loads(jsonStr)
            text_value = data[0]['text']
            print()
            await channel.send(text_value)
            print(bcolors.OKCYAN + "Succsesfully procesed: " + messagevar)        
##

#Start the
client.run(DiscordToken)
##