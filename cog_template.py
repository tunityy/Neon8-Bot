import discord
from discord.ext import commands
from discord.ext.commands import Cog, command

# Change each instance of NAMEHERE (3) to the name of the cog.
# Line 7(class), in tuples can include a name for the cog that will show up in the .help menu

class NAMEHERE(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('NAMEHERE cog for bot is online.')


    ### COMMANDS ###

    @command()
    async def generic(self, ctx):
        await ctx.send("This is a generic message, to use as an example.")


def setup(client):
    client.add_cog(NAMEHERE(client))