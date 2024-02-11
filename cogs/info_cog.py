import discord
from utils.createEmbed import create_embed
from discord.commands import slash_command
from discord.ext import commands

from utils.getSystemInfo import get_system_info


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def info(self, ctx):
        cpu_info, mem_info, disk_info = get_system_info()
        embed = create_embed(
            description="",
            title="System Information",
            color=discord.Color.nitro_pink(),
            fields=[
                {"name": "CPU", "value": f"Name: {cpu_info['name']}\nLoad: {cpu_info['load_percent']}%\nCores: {cpu_info['cores']}"},
                {"name": "Memory", "value": f"Total RAM: {mem_info['total_ram']}\nUsed RAM: {mem_info['used_ram']}\nRAM Usage: {mem_info['ram_percent']}%"},
                {"name": "Disk", "value": f"Total Disk: {disk_info['total_disk']}\nUsed Disk: {disk_info['used_disk']}\nDisk Usage: {disk_info['disk_percent']}%"}
            ]
        )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(InfoCog(bot))
