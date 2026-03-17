import os
import discord
from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # This sends the new message that the bot WILL own
        msg = await channel.send("⏳ Initializing ABR Server Status...")
        print("-------------------------------")
        print(f"NEW MESSAGE ID: {msg.id}")
        print("-------------------------------")
        print("COPY THE NUMBER ABOVE AND PUT IT IN GITHUB SECRETS!")
    await bot.close()

bot.run(TOKEN)
