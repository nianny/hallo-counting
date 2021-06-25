import discord
from discord.ext import commands
from client import *
import os
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("firebaseAuth.json")
firebase_admin.initialize_app(cred)

client = Client(command_prefix="n!", intents=discord.Intents.all(), help_command=None, allowed_mentions=discord.AllowedMentions.all())
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('n! help'))
    print("We have logged in as {0.user}".format(client))

client.run(os.getenv('niannybot'))