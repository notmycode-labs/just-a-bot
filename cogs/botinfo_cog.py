import os
import platform
import discord
import git
from utils.createEmbed import create_embed
from discord.commands import slash_command
from discord.ext import commands


repo = git.Repo(os.getcwd())



class BotInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest_commit = repo.head.commit

    @slash_command()
    async def botinfo(self, ctx):
        embed = create_embed(
        title=f"Bot information",
        description="",
        color=discord.Color.purple(),
        fields=[
            {'name': 'Python Version', 'value': platform.python_version()},
            {'name': 'Pycord Version', 'value': discord.__version__},
            {'name': 'Git commit', 'value': f"Commit hash: {self.latest_commit.hexsha}\nAuthor: {self.latest_commit.author.name}\nCommit Date: {self.latest_commit.authored_datetime}\nCommit msg: {self.latest_commit.message}"}
        ],
    )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(BotInfoCog(bot))