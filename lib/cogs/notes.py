import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord import Embed, Member
from lib.notes import fwrite_note, db_read_note, flist_notes, fdel_note, updateable_check, fupdate_note
# from lib.db.db import fwrite_note, db_read_note, flist_notes, fdel_note, updateable_check, fupdate_note
from datetime import datetime

class Notes(Cog):
    def __init__(self, client):
        self.client = client

    ### EVENTS ###
    
    @Cog.listener()
    async def on_ready(self):
        print('Notes cog for bot is online.')


    ### COMMANDS ###

    @command(aliases=['write', 'write note', 'writenote', 'make note', 'makenote', 'note'])
    async def write_note(self, ctx, note_title, *, args=None):
        if args is None:
            await ctx.send("Error: you can't write an empty note!")
        else:
            result = fwrite_note(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, note_title, args)
            if result == 'Repeat title':
                await ctx.send("There is already a note with that name.")
            elif result is None:
                await ctx.send("Oops, something went wrong.")
            else:
                await ctx.send(f'''Note titled "{result}" has been saved.''')


    @command(aliases=['read', 'see_note', 'seenote', 'readnote'])
    async def read_note(self, ctx, note_title):
        result = db_read_note(note_title, ctx.author.guild.id)

        if result is None:
            await ctx.send("That note doesn't exist.")
        else:
            embed = Embed(title=note_title,
                        description=f"*Written by {result[1]} on {result[2][:-10]} at {result[2][11:16]}*\n\n\n{result[0]}\n\u200b",
                        colour=discord.Colour.random(),
                        timestamp=datetime.utcnow())              
            embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.guild.get_member(result[3]).avatar_url)
            await ctx.send(embed=embed)


    @command(aliases=['listnotes', 'note_list', 'notelist', 'notes'])
    async def list_notes(self, ctx):
        result = flist_notes(ctx.author.guild.id, True, 5)
        if result is None:
            await ctx.send("There are no notes to view. Why not try writing one of your own? Use the command `.write (noteTitle) (note contents)` to write a note.")
        else:
            embed = Embed(title="Here are the notes available to read:",
                        description='Type `.read (note title)` without brackets to read that note.',
                        colour=discord.Colour(0x9f6231),
                        timestamp=datetime.utcnow())
            embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            embed.set_image(url='https://cdn.discordapp.com/attachments/823615456605896754/834291407807709224/pen_and_ink.jpg')
            fields = result
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)


    @command(aliases=['delnote', 'deletenote', 'delnotes', 'deletenotes', 'delete_notes'])
    async def delete_note(self, ctx, *, note_title):
        await ctx.send(f'''
This command will **permanently delete** "{note_title}" from the database. The contents cannot be recovered once this action has been completed.\n
Please confirm by typing "yes". Type anything else to cancel.
        ''')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        msg = await self.client.wait_for("message", check=check)
        confirmation = msg.content

        result = fdel_note(note_title, confirmation, ctx.author.guild.id)
        print(result)
        if result == 'Cancelled':
            await ctx.send("Cancelled, no notes have been deleted.")
        elif result == 'Something went wrong':
            await ctx.send("Oops, something went wrong.")
        elif result == None:
            await ctx.send('Error: Note was not deleted because note does not exist')
        else:
            if len(result) == 3:
                await ctx.send(f'''--- __**Error**: Unable to delete all notes__ ---\n
**Successfully Deleted**:  {', '.join(result[1])}
**Could Not Delete**:  {', '.join(result[2])}''')
            else:
                if len(result[1]) == 1:
                    await ctx.send(f'''Note titled "{result[0]}" has been deleted.''')
                elif len(result[1]) == 2:
                    await ctx.send(f'''Notes titled "{result[1][0]}" and "{result[1][1]}" have been deleted''')
                elif len(result[1]) > 2:
                    most_res_list = [f'"{res}"' for res in result[1][:-1]]
                    most_results = ', '.join(most_res_list)
                    last_result = f'"{result[1][-1]}"'
                    await ctx.send(f'''Notes titled {most_results}, and {last_result} have been deleted''')


    @command(aliases=['updatenote', 'change_note', 'changenote', 'modify_note', 'modifynote', 'editnote', 'edit_note'])
    async def update_note(self, ctx, notetitle):
        # meep = updateable_check(notetitle)
        meep = fupdate_note(notetitle, ctx.author.guild.id)
        await ctx.send(f"{meep}")


def setup(client):
    client.add_cog(Notes(client))