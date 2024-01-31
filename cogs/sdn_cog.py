import json
import os
from discord.commands import slash_command
from discord.ext import commands
from utils.createEmbed import create_embed


class SdnInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command()
    async def subdomains(self, ctx):
        file_path = os.path.join(os.getcwd(), 'data', 'public-sdn.json')
        with open(file_path, 'r') as file:
            data = json.load(file)

        fields = [{'name': entry['domain'], 'value': entry['desc'], 'inline': False} for entry in data]
        embed = create_embed(title="Public Subdomain Information", description="", fields=fields)

        await ctx.respond(embed=embed)
        
        

def setup(bot):
    bot.add_cog(SdnInfoCog(bot))