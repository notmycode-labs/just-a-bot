import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.createEmbed import create_embed
import requests

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("OWM_KEY")

    @slash_command(name="weather", description="Get weather information for a location.")
    async def weather(self, ctx, location: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric&lang=en"
        response = requests.get(url)
        data = response.json()
        print(data)
        if response.status_code == 200:
            weather_info = {
                "Location": data['name'],
                "Weather": data['weather'][0]['description'].capitalize(),
                "Temperature": f"{data['main']['temp']}°C",
                "Feels Like": f"{data['main']['feels_like']}°C",
                "Humidity": f"{data['main']['humidity']}%",
                "Wind Speed": f"{data['wind']['speed']} m/s"
            }

            embed_data = {
                "title": f"Weather Information for {data['name']}",
                "color": discord.Color.blue(),
                "fields": []
            }

            for key, value in weather_info.items():
                embed_data["fields"].append({"name": key, "value": value, "inline": False})

            embed = create_embed(**embed_data)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Failed to fetch weather information. Please try again later.")

def setup(bot):
    bot.add_cog(WeatherCog(bot))
