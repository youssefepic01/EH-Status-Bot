import os
import discord
import requests
from discord.ext import commands
from datetime import datetime

# These pull from your GitHub Secrets
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
MESSAGE_ID = int(os.environ['DISCORD_MESSAGE_ID'])

# This is your specific ID from the snippet you sent
MY_SERVER_ID = "4606-8ef3-aa7adcbe59bc" 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    try:
        # 1. Get the EH API data
        response = requests.get("https://api.emergency-hamburg.com/public/servers")
        all_servers = response.json()
        
        # 2. Find your specific server
        target = next((s for s in all_servers if MY_SERVER_ID in s.get('privateServerId', '')), None)
                
        if target:
            players = target.get('currentPlayers', 0)
            max_p = target.get('maxPlayers', 44)
            owner = target.get('ownerName', 'medo230y')
            code = target.get('code', 'TBm2HgcGtf')

            # 3. Create the design (Matches your image)
            embed = discord.Embed(title="🚨 BORDER RP 🚧 🇺🇸", color=0x2ecc71)
            embed.add_field(name="📶 Status", value="Online", inline=False)
            embed.add_field(name="🎮 Players", value=f"`{players} / {max_p}`", inline=False)
            embed.add_field(name="👑 Owner", value=owner, inline=False)
            embed.add_field(name="🔗 Server Code", value=f"`{code}`", inline=False)
            
            # Set thumbnail to your Roblox Avatar from the API
            avatar_url = target.get('ownerProfileUrl', '')
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)

            embed.set_footer(text=f"Powered by BORDER RP • Last updated: {datetime.now().strftime('%I:%M %p')}")

            # 4. Edit the Discord Message
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(MESSAGE_ID)
            await msg.edit(content=None, embed=embed)
            print("Successfully updated!")
        else:
            print("Server not found in API. Is it empty or offline?")
            
    except Exception as e:
        print(f"Error occurred: {e}")
    
    await bot.close()

bot.run(TOKEN)
