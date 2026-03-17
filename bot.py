import os
import discord
from discord.ext import commands

# These pull from your GitHub Secrets
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])

# Basic setup to get the bot online
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # 1. Get the channel using the ID from your Secrets
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        # 2. The bot sends a fresh message that IT owns
        msg = await channel.send("🚀 **ABR Server Status Initializing...**\nThis message will be updated every 5 minutes.")
        
        # 3. This prints the ID into your GitHub Actions console
        print("\n" + "="*30)
        print(f"SUCCESS! NEW MESSAGE ID: {msg.id}")
        print("="*30 + "\n")
        print("1. Copy the number above.")
        print("2. Go to GitHub Settings -> Secrets -> Actions.")
        print("3. Update 'DISCORD_MESSAGE_ID' with this number.")
    else:
        print("ERROR: Could not find the channel. Check your DISCORD_CHANNEL_ID secret.")

    # Close the bot after sending the message
    await bot.close()

bot.run(TOKEN)
