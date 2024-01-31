import platform
import discord
from utils.createEmbed import create_embed
from discord.commands import slash_command
from discord.ext import commands




class BotInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def botinfo(self, ctx):
        embed = create_embed(
        title=f"Bot information",
        description="",
        color=discord.Color.purple(),
        fields=[
            {'name': 'Python Version', 'value': platform.python_version()},
            {'name': 'Pycord Version', 'value': discord.__version__}
        ],
    )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(BotInfoCog(bot))