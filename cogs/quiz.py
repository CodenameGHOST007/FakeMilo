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
        self.match_parti = []
        self.curr_matchno = 1
        self.total_matches = 0
        self.match_ongoing = False

        #match_parti[match_no] -> determines the winner of the match number <match_no>
    #    
    #                 1
    #             /       \
            
    #         2               3

    #     /       \          /       \  
        
    # 4            5      6           7
        
    #     example 2 stores the winner of match between 4 and 5 (Initially it is -1)
    #     similarly 1 stores winner of march between 2 and 3
    #     

    async def initialise_parti(self,v , l , r,parti):
        if r<l:
            return
        if l == r:
            self.match_parti[v] = parti[l]
            return
        else:
            self.total_matches=self.total_matches+1
            self.match_parti[v] = -1
            mid = (l + r) // 2
            await self.initialise_parti(2*v , l , mid,parti)
            await self.initialise_parti(2*v+1 , mid+1 , r,parti)

    async def find_opponents(self,matchNumber):
        #if match_parti[2*matchNumber] is not -1 and match_parti[2*matchNumber+1] is not -1:
        return [self.match_parti[2*matchNumber] , self.match_parti[2*matchNumber+1]]
        #return [-1 , -1]
    
    
    async def get_schedule(self,ctx):
        embed = discord.Embed(title="Fake Milos Quiz Match Schedule " , color=discord.Color.blurple())
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        
        for i in range(0,self.total_matches):
            res=await self.find_opponents(self.total_matches-i)
            if res[0]==-1:
                res[0]="TO BE DECIDED"
            else:
                res[0]=self.client.get_user(int(res[0])).mention
            if res[1]==-1:
                res[1]="TO BE DECIDED"
            else:
                res[1]=self.client.get_user(int(res[1])).mention
            res2=self.match_parti[self.total_matches-i]
            if res2==-1:
                res2="TO BE DECIDED"
            else:
                res2=self.client.get_user(int(res2)).mention
            embed.add_field(name='Match no. '+str(i+1),value='1> '+res[0]+'\n2> '+res[1]+'\n **WINNER IS** : '+res2,inline=False)
        return embed
    async def clean_tournament_stats(self):
        self.total_matches=0
        self.curr_matchno=1
        self.match_parti=[]
    
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def quiz(self, ctx,*,body: str=""):
        if self.match_ongoing:
            await ctx.channel.send("TOURNAMENT IS ONGOING. PLEASE FINISH IT FIRST")
        await self.clean_tournament_stats()
        if(body==""):
            await ctx.channel.send("Please Enter participants")
            return
        parti=body.split(' ')
        for i in range(0,len(parti)):
            try:
                parti[i]=parti[i][3:21]
            except:
                await ctx.channel.send("Pleawse downit break me")
                return
        print(parti)
        if(len(parti)<2):   
            await ctx.channel.send("Please Enter at least 2 participants")
            return

        random.shuffle(parti)

        for i in range(1,200):
            self.match_parti.append(-1)
        #make tournament bracket here
        await self.initialise_parti(1 , 0 , len(parti)-1,parti)
        embed= await self.get_schedule(ctx)
        await ctx.channel.send(embed=embed)
        self.match_ongoing=True

    @commands.cooldown(1, 2, commands.BucketType.channel)
    @commands.command(pass_context=True)
    async def schedule(self,ctx,arg: str=""):
        if self.total_matches==0:
            await ctx.channel.send("No match history")
            return
        embed=await self.get_schedule(ctx)
        await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.channel)
    @commands.command(pass_context=True)
    async def match(self,ctx,*,body: str=""):
        if self.match_ongoing==False:
            await ctx.channel.send("No match ongoing")
            return
        match_no=0
        try:
            match_no=int(body)  #assign match no
        except:
            await ctx.channel.send("Please enter proper match number.")
            return


        if match_no != self.curr_matchno :
            await ctx.channel.send("Next match up is "+str(self.curr_matchno))
            return
            #winner is decided and his index is in match_parti[1]
        
        partic = await self.find_opponents(self.total_matches-match_no+1)
        parti1=int(partic[0])
        parti2=int(partic[1])
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
            #print(message.author.id)
            #print(parti1)
            if((int(message.author.id)!=int(parti1) and int(message.author.id)!=int(parti2)) or message.channel.id!=ctx.channel.id):
                return False
            if message.content.upper()==q1[2]:
                return True
            else:
                return False
        resp=await self.client.wait_for('message',timeout=30,check=check)
        embed = discord.Embed(title="Fake Milos Quiz Match no. %s" %match_no, color=discord.Color.blurple(),
                                  description=q1[0])
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name="MATCH OVER",value="%s Won the match"%resp.author.mention)
        await ctx.channel.send(embed=embed)
        #update matching tables and stuff

        #let's say parti1 is the winner
        self.match_parti[self.total_matches-match_no+1] = resp.author.id
        self.curr_matchno += 1
        if self.curr_matchno>self.total_matches:
            self.match_ongoing=False
            embed = discord.Embed(title="Fake Milos Quiz TOURNAMENT OVER", color=discord.Color.blurple(),
                                  description=" ")
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            embed.add_field(name="**TOURNAMENT OVER**",value="%s Won the match"%resp.author.mention)
            await ctx.channel.send(embed=embed)
            
            


def setup(client):
    client.add_cog(Quiz(client))