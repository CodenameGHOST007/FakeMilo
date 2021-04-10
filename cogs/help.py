from discord.ext import commands 
import discord
from discord import Color , Embed , Game
from math import ceil
from humanfriendly import format_timespan
import random


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.info = {
            #to be done
        }

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if not isinstance(error, (commands.CommandNotFound, commands.CommandOnCooldown)):
            ctx.command.reset_cooldown(ctx)

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = ceil(error.retry_after)
            towait = format_timespan(seconds)
            await ctx.channel.send("**%s**, You can use this command again after %s." % (ctx.author.name, towait))
        elif isinstance(error, discord.Forbidden) and error.code == 50013:
            if ctx.channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.channel.send("Hey, looks like I don't have proper permissions to run the command properly. "
                                       "Please make sure I have atleast the following permissions and try again:\n"
                                       "`MAKE ME ADMIN ALREADY`.")
        elif isinstance(error,commands.MaxConcurrencyReached):
            await ctx.channel.send("Finish previous tournament first")
        else:
            print(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.client.change_presence(activity=Game(name="Translate in "+str(len(self.client.guilds))+" Servers "))    
        allowed = []
        for channel in guild.channels:
            if channel.permissions_for(guild.me).send_messages and channel.permissions_for(guild.me).embed_links:
                allowed.append(channel)
        if len(allowed) >= 1:
            to_post = allowed[0]
            for channel in allowed:
                if "general" in channel.name:
                    to_post = channel
                    break
            embed = discord.Embed(title="Fake Milo Help", color=discord.Color.dark_magenta(),
                                  description="Hey there, I am %s! My prefix is **m!**, or you can "
                                              "mention me to use my commands." % guild.me.mention)
            embed.set_author(name=str(guild.me), icon_url=guild.me.avatar_url)
            embed.set_footer(text="Requested by "+str(author), icon_url=ctx.author.avatar_url)
            embed.add_field(name="Important info",value="[Join my support server if you have problem using the commands!]()",inline=False)
            for k in self.info:
                embed.add_field(name=" <:GhostHug:644518464819560449> `%s`" %(k),value=self.info[k])
            #embed.add_field(name=":e_mail: Join Support server", value ="[Here!](<to be added>)",inline=False)
            #embed.add_field(name=":medal: Vote for me", value="[Here!](<to be added>)",inline=True)
            await to_post.send(embed=embed)
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        async with ctx.channel.typing():
            await ctx.channel.send("Pong! :white_check_mark:")

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True, name="invite", aliases=['server', 'support', 'about', 'botinfo'])
    async def invite(self, ctx):
        #using [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)!
        embed = discord.Embed(color=discord.Color.dark_blue(),
                              title="Fake Milos Info",
                              description = "Created by **CodenameGHOST#6330** "
                                            "\n\n[Add me to your server here!](https://discordapp.com/oauth2/authorize?client_id=830132289010532372&scope=bot&permissions=603286592)"
                                            "\n[Join my support server here!]()")
        embed.set_footer(text="Requested by "+str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def help(self, ctx, arg: str = ""):
        if arg == "":
            command_list = [k for k in self.info]
            #main_help = "\n".join("**m!%s**: %s" % (k, self.info[k]) for k in command_list[:5])
            #info_help = "\n".join("**m!%s**: %s" % (k, self.info[k]) for k in command_list[5:])
            embed = discord.Embed(title="Fake Milos Help", color=discord.Color.blurple(),
                                  description="Hey there, I am %s! My prefix is **m!**, or you can "
                                              "mention me to use my commands." % ctx.guild.me.mention)
            embed.set_author(name=str(ctx.guild.me), icon_url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Requested by "+str(ctx.author), icon_url=ctx.author.avatar_url)
            embed.add_field(name="Important info",value="[Join my support server if you have problem using the commands!]()",inline=False)
            for k in self.info:
                embed.add_field(name=" <:GhostHug:644518464819560449> `%s`" %(k),value=self.info[k])
            
            #embed.add_field(name=":notebook: Translation commands", value=main_help, inline=False)
            #embed.add_field(name=":gear: Info Commands", value=info_help, inline=False)
            await ctx.channel.send(embed=embed)
        else:
            found = None
            for command in self.client.commands:
                if command.name == arg or arg in command.aliases:
                    found = True
                    break
            if found:
                embed = discord.Embed(title="Help for "+command.name,
                                      description=self.info[command.name],
                                      color=discord.Color.dark_purple())
                syntax_dict = {" ": " "}
                #to be done
                embed.add_field(name="Syntax", value="`m!%s %s`" % (command.name,
                                                                  "" if command.name not in syntax_dict else syntax_dict[command.name]))
                if command.aliases:
                    embed.add_field(name="Aliases",
                                    value=", ".join("`m!%s`" % k for k in command.aliases), inline=False)
                embed.set_footer(text="Requested by "+str(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send(ctx.author.name+", No command called `"+arg+"` could be found!")


def setup(client):
    client.add_cog(Help(client))
