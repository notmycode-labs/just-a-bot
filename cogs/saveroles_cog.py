import os
import sqlite3
import discord
from discord.commands import slash_command
from discord.ext import commands
from utils.createEmbed import create_embed

cwd = os.getcwd()
db_path = os.path.join(cwd, 'data', 'roles.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS saved_roles
             (user_id INTEGER PRIMARY KEY, roles TEXT)''')
conn.commit()

class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="saveroles", description="Save user's roles.")
    async def save_roles(self, ctx):
        user = ctx.author
        roles = [role.id for role in user.roles]
        c.execute('''INSERT OR REPLACE INTO saved_roles (user_id, roles) VALUES (?, ?)''', (user.id, ",".join(map(str, roles))))
        conn.commit()
        
        embed_data = {
            "title": "Roles Saved",
            "description": "User's roles have been saved successfully.",
            "color": discord.Color.green()
        }
        embed = create_embed(**embed_data)
        await ctx.respond(embed=embed)

    @slash_command(name="getroles", description="Get user's saved roles.")
    async def get_roles(self, ctx, user: discord.User):
        user_id = user.id

        c.execute('''SELECT roles FROM saved_roles WHERE user_id = ?''', (user_id,))
        roles_data = c.fetchone()

        if roles_data:
            roles_ids = roles_data[0].split(",")
            roles = [ctx.guild.get_role(int(role_id)) for role_id in roles_ids if ctx.guild.get_role(int(role_id))]
            
            roles_mention = ", ".join([role.mention for role in roles])
            embed_data = {
                "title": f"Roles of User {user_id}",
                "description": f"User's roles: {roles_mention}",
                "color": discord.Color.blue()
            }
            embed = create_embed(**embed_data)
            await ctx.respond(embed=embed)
        else:
            embed_data = {
                "title": "No Saved Roles",
                "description": "This user does not have any saved roles.",
                "color": discord.Color.red()
            }
            embed = create_embed(**embed_data)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RoleCog(bot))
