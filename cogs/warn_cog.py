import os
import sqlite3
from discord.commands import slash_command
from discord.ext import commands
import discord

cwd = os.getcwd()

db_path = os.path.join(cwd, 'data', 'warns.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS warns
             (user_id INTEGER, reason TEXT)''')
conn.commit()

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, user: commands.MemberConverter, *, reason: str):
        c.execute('''INSERT INTO warns (user_id, reason) VALUES (?, ?)''', (user.id, reason))
        conn.commit()

        embed = discord.Embed(title="User Warning", color=discord.Color.red())
        embed.add_field(name="Warned User", value=user.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.author.send(embed=embed)
        else:
            await ctx.respond(embed=embed)

    @slash_command()
    @commands.has_permissions(manage_guild=True)
    async def latestwarn(self, ctx, user: commands.MemberConverter):
        c.execute('''SELECT reason FROM warns WHERE user_id = ? ORDER BY ROWID DESC LIMIT 1''', (user.id,))
        latest_warn = c.fetchone()

        if latest_warn:
            embed = discord.Embed(title="Latest Warning", color=discord.Color.red())
            embed.add_field(name="Reason", value=latest_warn[0], inline=False)
            
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.author.send(embed=embed)
            else:
                await ctx.respond(embed=embed)
        else:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.author.send(f"{user.mention} has no recorded warnings.")
            else:
                await ctx.respond(f"{user.mention} has no recorded warnings.")

    @slash_command()
    @commands.has_permissions(manage_guild=True)
    async def warninfo(self, ctx, user: commands.MemberConverter):
        c.execute('''SELECT reason FROM warns WHERE user_id = ?''', (user.id,))
        warnings = c.fetchall()

        warn_count = len(warnings)

        if warnings:
            embed = discord.Embed(title="Warning Information", color=discord.Color.red())
            embed.add_field(name="Total Warnings", value=warn_count, inline=False)
            for i, warn in enumerate(warnings):
                embed.add_field(name=f"Warning {i+1}", value=warn[0], inline=False)
            
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.author.send(embed=embed)
            else:
                await ctx.respond(embed=embed)
        else:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.author.send(f"{user.mention} has no recorded warnings.")
            else:
                await ctx.respond(f"{user.mention} has no recorded warnings.")


def setup(bot):
    bot.add_cog(WarnCog(bot))
