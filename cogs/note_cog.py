import os
import sqlite3
from discord.commands import slash_command
from discord.ext import commands

from utils.createEmbed import create_embed


cwd = os.getcwd()
db_path = os.path.join(cwd, 'data','notes.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS notes
             (user_id INTEGER PRIMARY KEY, note TEXT)''')
conn.commit()

class NoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def note(self, ctx, *, content: str):
        user_id = ctx.author.id
        note = content

        c.execute('''SELECT * FROM notes WHERE user_id = ?''', (user_id,))
        existing_note = c.fetchone()

        if existing_note:
            c.execute('''UPDATE notes SET note = ? WHERE user_id = ?''', (note, user_id))
            response_message = f"Note updated for {ctx.author.mention}."
        else:
            c.execute('''INSERT INTO notes (user_id, note) VALUES (?, ?)''', (user_id, note))
            response_message = f"Note saved for {ctx.author.mention}."

        conn.commit()

        embed = create_embed(title="Note", description=response_message)
        await ctx.respond(embed=embed)

    @note.error
    async def note_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = create_embed(title="Note", description="Please provide a note.")
            await ctx.respond(embed=embed)

    @slash_command()
    async def mynote(self, ctx):
        user_id = ctx.author.id

        c.execute('''SELECT note FROM notes WHERE user_id = ?''', (user_id,))
        note = c.fetchone()

        if note:
            embed = create_embed(title="Your Note", description=note[0])
            await ctx.respond(embed=embed)
        else:
            embed = create_embed(title="Your Note", description="You haven't saved any notes yet.")
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(NoteCog(bot))
