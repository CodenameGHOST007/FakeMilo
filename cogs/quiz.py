from discord.ext import commands 
import discord
from discord import Color , Embed , Game
from math import ceil
from humanfriendly import format_timespan
import util.trivia_api as api
import random


class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        #self.match_parti = [[]]
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def quiz(self, ctx,arg: str=""):
        if(str==""):
            await ctx.channel.send("Please Enter participants")
            return
        parti=str.split(' ')
        if(len(parti)>0):   #error here change
            await ctx.channel.send("Please Enter at least 2 participants")
            return
        
        #make tournament bracket here

    @commands.cooldown(1, 2, commands.BucketType.channel)
    @commands.command(pass_context=True)
    async def match(self,ctx,arg: str=""):
        match_no=0
        try:
            match_no=0  #assign match no
        except:
            await ctx.channel.send("Please enter proper match number.")
            return
        #parti1=match_parti[match_no][0]
        #parti2=match_parti[match_no][1]
        Api=api.API()
        q1=await Api.get_trivia()          #FORMAT: question, array of options, answer option, field of question
        embed = discord.Embed(title="Fake Milos Quiz Match no. %s" %match_no, color=discord.Color.blurple(),
                                  description=q1[0])
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        #embed.set_footer(text="Requested by "+str(ctx.author), icon_url=ctx.author.avatar_url)
        l=['A','B','C','D','E','F','G']
        tag=0
        for i in q1[1]:
            embed.add_field(name="\0",value="**%s> %s**"%(l[tag],i),inline=True)
            tag=(int(tag)+1)
        await ctx.channel.send(embed=embed)
        def check(message):
            #modify check using parti1 and parti2 later
            if(message.author.id!=ctx.author.id or message.channel.id!=ctx.channel.id):
                return False
            if message.content.upper() in l:
                return True
            else:
                return False
        resp=await self.client.wait_for('message',timeout=30,check=check)
        if resp.content.upper()==q1[2]:
            await ctx.channel.send("You answered correctly")
        else:
            await ctx.channel.send("WRONG ANS")

        #update matching tables and stuff




def setup(client):
    client.add_cog(Quiz(client))