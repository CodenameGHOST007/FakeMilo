from discord.ext.commands import Bot, when_mentioned_or
from discord import Embed, Color, File
from os import listdir
from os.path import isfile, join
from discord import Game
import random
from os import environ
from dotenv import load_dotenv

load_dotenv()

description = '''Fake Milos'''
cogs_dir = "cogs"
client = Bot(description="Discord Bot by Me and me only smh", command_prefix=when_mentioned_or("m!"))
client.remove_command("help")

@client.event
async def on_ready():
    #await client.change_presence(activity=Game(name=" FAKE MILOS "))
    await client.change_presence(activity=Game(name="Hacking in "+str(len(client.guilds))+" Servers "))
    #emoji.cone=emoji.Emoji(client)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            client.load_extension("cogs." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            print(str(e))

    token = environ.get('F_TOKEN')
    #print(token)
    client.run(token)