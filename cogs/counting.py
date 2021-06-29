import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore
import concurrent.futures
import asyncio

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = firestore.client()
        self.data = {}
        docs = self.db.collection(u'servers').stream()
        for doc in docs:
            self.data[doc.id] = doc.to_dict()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.channel.name.lower() == "hallocounting":
            string = message.content.lower()
            string = string.split(" ")[0]
            string = string.split("_")[0]
            string = string.split("*")[0]
            if string.isdigit():
                if str(message.guild.id) not in self.data:
                    dict2 = {
                        "count": 0,
                        "lastuser": None,
                        "highestcount": 0
                    }
                else:
                    dict2 = self.data[str(message.guild.id)]
                num = int(string)
                if not (num == dict2["count"]+1):
                    dict2["count"] = 0
                    dict2["lastuser"] = None
                    self.data[str(message.guild.id)] = dict2
                    await message.add_reaction("❌")
                    embed = discord.Embed(
                        title="Wrong Count",
                        description=f"{message.author.mention} messed up the count at **{dict2['count']}**. The next count for this server is **1**.",
                        colour = self.client.primary_colour
                    )
                    await message.channel.send(embed=embed)
                    await message.channel.edit(topic=f"Count: {dict2['count']}")
                    
                    
                    
                elif (message.author.id==dict2["lastuser"]):
                    dict2["count"] = 0
                    dict2["lastuser"] = None
                    self.data[str(message.guild.id)] = dict2
                    await message.add_reaction("❌")
                    embed = discord.Embed(
                        title="You cannot count twice in a row",
                        description=f"{message.author.mention} messed up the count at **{dict2['count']}**. The next count for this server is **1**.",
                        colour = self.client.primary_colour
                    )
                    await message.channel.send(embed=embed)
                    await message.channel.edit(topic=f"Count: {dict2['count']}")
                    
                else:
                    if (num > dict2["highestcount"]):
                        dict2["highestcount"] = num
                        self.data[str(message.guild.id)] = dict2
                        await message.add_reaction("☑️")
                        await message.channel.edit(topic=f"Count: {dict2['count']}")
                    else:
                        dict2["count"] = num
                        dict2["lastuser"] = message.author.id
                        self.data[str(message.guild.id)] = dict2
                        await message.add_reaction("✅")
                        await message.channel.edit(topic=f"Count: {dict2['count']}")

                self.db.collection(u'servers').document(str(message.guild.id)).set(dict2)

def setup(client):
    client.add_cog(Counting(client))