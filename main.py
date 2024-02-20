
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from utils.getmsg import get_message
from discord_webhook import DiscordWebhook

load_dotenv()
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    
    print(f"🚀 {bot.user.name} is online!")
    print(f"🔧 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} servers")
    print(f"🤖 Running on Pycord v{discord.__version__}")
    update_status.start()
    #await bot.change_presence(activity=discord.Game(name="Pipe bomb", type=3))

@tasks.loop(seconds=30)
async def update_status():
    latency = bot.latency * 1000
    await bot.change_presence(activity=discord.Game(name=f'Pipe bomb - {latency:.2f}ms'))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot: return

    webhook = DiscordWebhook(url=os.getenv("WEBHOOK_LOG_URL"), content=f"```{get_message(message.channel.id, message.id)}```")
    response = webhook.execute()



for filename in os.listdir('./cogs'):
    if filename.endswith('_cog.py'):
        module = f'cogs.{filename[:-3]}'
        print(f"📑 Module {module} loaded!")
        bot.load_extension(module)
        
 
if __name__ == '__main__':
    bot.run(os.getenv("BOT_TOKEN"))