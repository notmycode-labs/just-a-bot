import os
from discord.commands import slash_command
from discord.ext import commands

from utils.createEmbed import create_embed

class AboutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def about(self, ctx):
        about_text = "We are stupid Thailand teams for making some random stuff and creative stuff about programming, coding, computer and more!"

        links = [
            {"name": "Website", "value": "https://notmycode.dev"},
            {"name": "GitHub", "value": "https://github.com/notmycode-dev"}
        ]

        about_embed = create_embed(title="About notmycode.dev", description=about_text, fields=links)

        await ctx.respond(embed=about_embed)



def setup(bot):
    bot.add_cog(AboutCog(bot))