import os
import sqlite3
from datetime import datetime
from discord.commands import slash_command
from discord.ext import commands

cwd = os.getcwd()
db_path = os.path.join(cwd, 'data', 'deletemsg.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS deleted_messages
             (message_id INTEGER PRIMARY KEY, author_id INTEGER, content TEXT, delete_date TEXT, channel_id INTEGER)''')
conn.commit()

class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit: int = 10):
        limit = min(limit, 200)
        messages = await ctx.channel.history(limit=limit + 1).flatten()
        deleted_message_count = len(messages) - 1
        delete_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        for message in messages:
            c.execute('''INSERT INTO deleted_messages (message_id, author_id, content, delete_date, channel_id) VALUES (?, ?, ?, ?, ?)''', (message.id, message.author.id, message.content, delete_date, message.channel.id))
        conn.commit()
        await ctx.channel.delete_messages(messages)

        await ctx.respond(f"{deleted_message_count} messages deleted.", delete_after=5)

def setup(bot):
    bot.add_cog(ClearCog(bot))
