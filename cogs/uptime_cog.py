import discord
import time
from datetime import datetime
from discord.ext import commands
from discord.commands import slash_command
from utils.createEmbed import create_embed

class UptimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = 0

    @slash_command(name="uptime", description="Check the bot's uptime.")
    async def uptime(self, ctx):
        current_time = time.time()
        uptime_seconds = round(current_time - self.start_time)
        uptime_string = self.format_seconds(uptime_seconds)
        
        embed_data = {
            "title": "Bot Uptime",
            "description": f"The bot has been running for: {uptime_string}",
            "color": discord.Color.blue()
        }
        embed = create_embed(**embed_data)
        await ctx.respond(embed=embed)

    def format_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def setup(bot):
    bot.add_cog(UptimeCog(bot))
