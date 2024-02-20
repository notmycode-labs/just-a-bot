import os
from datetime import datetime
from discord.commands import slash_command
from discord.ext import commands

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, 'deleted_messages.txt')

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
        with open(file_path, 'a') as file:
            for message in messages:
                file.write(f"{message.id},{message.author.id},{message.content},{delete_date},{message.channel.id}\n")
        await ctx.channel.delete_messages(messages)

        await ctx.respond(f"{deleted_message_count} messages deleted.", delete_after=5)

def setup(bot):
    bot.add_cog(ClearCog(bot))
