import os
import discord
import requests
from discord.ext import commands
import time
import asyncio

# CONFIGURATION
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
MESSAGE_ID = int(os.environ['DISCORD_MESSAGE_ID'])
MY_SERVER_ID = "4606-8ef3-aa7adcbe59bc" 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class JoinButton(discord.ui.View):
    def __init__(self, join_code):
        super().__init__()
        # PlaceID from your screenshot
        url = f"https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode%3D{join_code}"
        self.add_item(discord.ui.Button(label='Join Server', url=url, emoji='🔗', style=discord.ButtonStyle.link))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}. Updating status...")
    try:
        # 1. Get Roblox Data
        response = requests.get("https://api.emergency-hamburg.com/public/servers", timeout=10)
        all_servers = response.json()
        target = next((s for s in all_servers if MY_SERVER_ID in s.get('privateServerId', '')), None)
                
        if target:
            players = target.get('currentPlayers', 0)
            max_p = target.get('maxPlayers', 44)
            owner = target.get('ownerName', 'medo230y')
            code = "iz99bb68" # Your updated code

            # 2. Build the Embed
            embed = discord.Embed(
                title="🚨 BORDER RP 🚧 🇺🇸", 
                description="**Serious Roleplay Community**",
                color=0x2ecc71 
            )
            
            embed.add_field(name="📶 Status", value="🟢 **Online**", inline=True)
            embed.add_field(name="🎮 Players", value=f"`{players} / {max_p}`", inline=True)
            embed.add_field(name="👑 Owner", value=f"[{owner}](https://www.roblox.com/users/{target.get('ownerId')}/profile)", inline=False)
            embed.add_field(name="🔑 Join Code", value=f"`{code}`", inline=False)
            
            # Dynamic Timestamp (Shows "5 minutes ago")
            sync_time = int(time.time())
            embed.add_field(name="🕒 Last Sync", value=f"<t:{sync_time}:R>", inline=False)
            
            if target.get('ownerProfileUrl'):
                embed.set_thumbnail(url=target.get('ownerProfileUrl'))

            embed.set_footer(text="ABR Development • Real-Time Monitor", icon_url=target.get('ownerProfileUrl'))

            # 3. Update Discord
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(MESSAGE_ID)
            await msg.edit(content=None, embed=embed, view=JoinButton(code))
            print("Update Successful!")
        else:
            print("Server not found. Is it offline?")
            
    except Exception as e:
        print(f"Error occurred: {e}")
    
    # 4. Force Close (Crucial for GitHub Actions)
    await bot.close()

# Start the bot
bot.run(TOKEN)
