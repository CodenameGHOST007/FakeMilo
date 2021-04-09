from discord.ext import commands
import discord
from discord import Color, Embed, Game
from math import ceil
from humanfriendly import format_timespan
import random
import asyncio
import traceback
import discord
import inspect
import textwrap
import importlib
from contextlib import redirect_stdout
import io
import os
import re
import sys
import copy
import time
import subprocess
from typing import Union, Optional

# to expose to the eval command
import datetime
from collections import Counter

class Exe2(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self._last_result = None


    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if (content.startswith('```') or content.startswith('\n```')) and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def exe2(self, ctx, *, body: str = ""):
        if(ctx.author.id==304898295451484171 or ctx.author.id==519879218402689024):            
            print("inside exe2", ctx.author.id, body)
            """Evaluates a code"""

            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(body)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('\u2705')
                except:
                    pass

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')
        else:
            async with ctx.channel.typing():
                await ctx.channel.send("Not permitted!")
            return

def setup(client):
    client.add_cog(Exe2(client))
