import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import FFmpegPCMAudio
from discord import TextChannel
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
    
    @slash_command(name="playsound", description="Play any sound from an MP3 link in the voice channel.")
    async def play_sound(self, ctx, mp3_link: str):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            try:
                voice.play(discord.FFmpegOpusAudio(mp3_link))
                await ctx.respond("Bot is playing the sound")
            except Exception as e:
                await ctx.respond(f"An error occurred: {e}")
        else:
            await ctx.respond("Bot is already playing a sound")

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
