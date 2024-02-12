import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from utils.createEmbed import create_embed

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @slash_command(name="join", description="Join the user's voice channel.")
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    
    @slash_command(name="play", description="Play sound from a YouTube URL.")
    async def play(self, ctx, url: str):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.respond("Bot is playing")
        else:
            await ctx.respond("Bot is already playing")

    @slash_command(name="resume", description="Resume playback.")
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.respond("Bot is resuming")

    @slash_command(name="pause", description="Pause playback.")
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.respond("Bot has been paused")

    @slash_command(name="stop", description="Stop playback.")
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.respond("Stopping...")

def setup(bot):
    bot.add_cog(MusicCog(bot))
