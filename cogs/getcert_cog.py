from utils.createEmbed import create_embed
from utils.getCert import get_certificate_info
from discord.commands import slash_command
from discord.ext import commands


class GetCertCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="getcert", description="Get certificate information for a URL")
    async def getcert(self, ctx, url: str):
        certificate_info = get_certificate_info(url)
        embed = create_embed(
            description="",
            title=f"Certificate Information for {url}",
            fields=[{"name": str(key), "value": str(value)} for key, value in certificate_info.items()]
        )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(GetCertCog(bot))