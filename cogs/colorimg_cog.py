import discord
from discord.commands import slash_command
from discord.ext import commands
from PIL import Image, ImageDraw
import io


class ColorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def color(self, ctx, color_code: str):
        rgb_color = tuple(int(color_code[i:i + 2], 16) for i in (0, 2, 4))
        image = Image.new('RGB', (128, 128), rgb_color)
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)

        await ctx.respond(file=discord.File(image_buffer, filename='color.png'))

def setup(bot):
    bot.add_cog(ColorCog(bot))