from discord.ext import commands 
import discord
from discord import Color , Embed , Game
import pymongo
from pymongo import MongoClient
import os

cluster = MongoClient(os.environ.get('CONNECTION_URL'))
db = cluster["FakeMiloDB"]

collection = db["BotUsers"]

class Player(commands.Cog):
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def highest_scores(self , ctx):
        embed = discord.Embed(title="Fake Milos Highest Scorers" , color=discord.Color.blurple())
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        count = 0
        for x in collection.find().sort('won'):
            if count == 10:
                break
            # print(x['id'] + x['won'])
            embed.add_field(name=x['name'],value='has won ' + str(x['won']) + ' matches',inline=False)
            count += 1
            # await ctx.channel.send(str(x['id']) + ' ' + str(x['won']) + '\n')
        
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Player(client))