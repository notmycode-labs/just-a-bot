import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.createEmbed import create_embed

class MemberCountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="membercount", description="Counts the members in the server.")
    async def count_members(self, ctx):
        guild = ctx.guild
        if guild:
            total_members = guild.member_count

            embed_data = {
                "title": "Member Count",
                "color": discord.Color.blue(),
                "fields": [
                    {"name": "Total Members", "value": str(total_members), "inline": False}
                ]
            }

            embed = create_embed(**embed_data)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("This command can only be used in a server.")

def setup(bot):
    bot.add_cog(MemberCountCog(bot))
