import discord
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord import Embed, Member
from lib.notes import fwrite_note, db_read_note, flist_notes, fdel_note, updateable_check, fupdate_note, edit_note_check
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

    @commands.group(invoke_without_command=True, aliases=['notes'])
    async def note(self, ctx):
        await ctx.send("""Write and read notes, show a list of all notes, and edit or delete notes. Available commands:
`.note write <note_title> <note contents>`\n`.note read <note_title>`\n`.note list`\n`.note edit <note_title>`\n`.note delete <note_title>`""")
# TODO: Make this nicer


    @note.command(name='help', aliases=['info'])
    async def help_note(self, ctx):
        await ctx.send("""Write and read notes, show a list of all notes, and edit or delete notes. Available commands:
`.note write <note_title> <note contents>`\n`.note read <note_title>`\n`.note list`\n`.note edit <note_title>`\n`.note delete <note_title>`""")
# TODO: Make this nicer


    # # I'm sure there's a better name for this, but whatever. It works for now.
    # @note.command(aliases=['uneditable', 'unchangeable', 'static', 'makestatic', 'locked', 'writelocked'])
    # async def write_uneditable(self, ctx, note_title, *, args=None):
    #     if args is None:
    #         await ctx.send("Error: you can't write an empty note!")
    #     else:
    #         result = fwrite_note(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, note_title, args)
    #         if result == 'Repeat title':
    #             await ctx.send("There is already a note with that name.")
    #         elif result is None:
    #             await ctx.send("Oops, something went wrong.")
    #         else:
    #             await ctx.send(f'''Note titled "{result}" has been saved.''')


    @note.command(aliases=['make', 'new'])
    async def write(self, ctx, note_title, *, args=None):
        if args is None:
            await ctx.send("Error: you can't write an empty note!")
        else:
            result = fwrite_note(ctx.author, ctx.author.display_name, ctx.author.id, ctx.author.guild.id, note_title, args, True)
            if result == 'Repeat title':
                await ctx.send("There is already a note with that name.")
            elif result is None:
                await ctx.send("Oops, something went wrong.")
            else:
                await ctx.send(f'''Note titled "{result}" has been saved.''')


    @note.command(aliases=['see', 'view', 'select'])
    async def read(self, ctx, note_title):
        result = db_read_note(note_title, ctx.author.guild.id, True)
        if result is None:
            await ctx.send("That note doesn't exist.")

        else:
            if result[4] == 'False':
                descr = f"*Created by {result[1]} on {result[2][:-10]} at {result[2][11:16]}*\n\n\n{result[0]}\n\u200b"
            elif result[4] == 'True':
                if result[3] == result[7]:
                    descr = f"""*Created by {result[1]} on {result[2][:-10]}*\n
                            --- *Edited on {result[8][:10]}* ---
                            \n\n{result[0]}\n\u200b"""
                elif result[3] != result[7]:
                    editor_nick = ctx.author.guild.get_member(result[7]).display_name
                    descr = f"""*Created by {result[1]} on {result[2][:-10]}*\n
                            --- *Edited by {editor_nick} ({result[5][:-5]}) on {result[8][:10]}* ---
                            \n\n{result[0]}\n\u200b"""

            embed = Embed(title=note_title,
                        description=descr,
                        colour=discord.Colour.random(),
                        timestamp=datetime.utcnow())              
            embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.guild.get_member(result[3]).avatar_url)
            # embed.add_field(name="\u200b", value=f"Length: {len(result[0])} characters", inline=False)
            await ctx.send(embed=embed)


    @note.command(name="list", aliases=['all'])
    async def list_notes(self, ctx):
        result = flist_notes(ctx.author.guild.id, True, 5)
        if result is None:
            await ctx.send("There are no notes to view. Why not try writing one of your own? Use the command `.note write (noteTitle) (note contents)` to write a note.")
        else:
            embed = Embed(title="Here are the notes available to read:",
                        description='Type `.note read (note title)` without brackets to read that note.',
                        colour=discord.Colour(0x9f6231),
                        timestamp=datetime.utcnow())
            embed.set_footer(text=f"Requested by:  {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            embed.set_image(url='https://cdn.discordapp.com/attachments/823615456605896754/834291407807709224/pen_and_ink.jpg')
            fields = result
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)


    # TODO: 
    @note.command(name='delete', aliases=['remove', 'del'])
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
        await ctx.send(result)


    @note.command(name='edit', aliases=['update', 'change', 'modify'])
    async def edit_note(self, ctx, note_title):
        ### Plain text version ###
        # check_note = edit_note_check(note_title, ctx.author.guild.id, ctx.author.id, False, False)
        # if check_note[0] == 'Problem':
        #     await ctx.send(check_note[1])
        # else:
        #     await ctx.send(check_note)

        check_note = edit_note_check(note_title, ctx.author.guild.id, ctx.author.id)
        if check_note[0] == 'Problem':
            await ctx.send(check_note[1])

        else:
            embed = Embed(title=check_note[0],
                        description=check_note[1],
                        colour=discord.Colour.random(),
                        timestamp=datetime.utcnow())
            embed.set_footer(text='\u200b', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.guild.get_member(check_note[2]).avatar_url)

            fields = check_note[3]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.client.wait_for("message", check=check)
            note_content = msg.content
            # if note_content.lower() in ['no', 'cancel', 'n'] or note_content[0] == '.': # This might work too? And be easier to read.
            if note_content.lower() == 'no' or note_content.lower() == 'cancel' or note_content.lower() == 'n' or note_content[0] == '.':
                await ctx.send("Edit cancelled, note is unchanged.")
            else:
                result = fupdate_note(ctx.author.guild.id, ctx.author.id, ctx.author, ctx.author.display_name, note_title, note_content, True)
                await ctx.send(result)


    # @note.command(names='rename')
    # async def rename_note(self, ctx, old_title, new_title):
    #     pass


def setup(client):
    client.add_cog(Notes(client))