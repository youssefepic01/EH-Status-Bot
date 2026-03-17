import os
import discord
import requests
from discord.ext import commands
import time

# --- CONFIG ---
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
MESSAGE_ID = int(os.environ['DISCORD_MESSAGE_ID'])
MY_SERVER_ID = "4606-8ef3-aa7adcbe59bc" 
JOIN_CODE = "iz99bb68"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class JoinButton(discord.ui.View):
    def __init__(self, join_code):
        super().__init__()
        url = f"https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode%3D{join_code}"
        self.add_item(discord.ui.Button(label='Join Server', url=url, emoji='🎮', style=discord.ButtonStyle.link))

@bot.event
async def on_ready():
    print(f"Updating ABR Status...")
    try:
        response = requests.get("https://api.emergency-hamburg.com/public/servers", timeout=10)
        target = next((s for s in response.json() if MY_SERVER_ID in s.get('privateServerId', '')), None)
        
        if target:
            players = target.get('currentPlayers', 0)
            max_p = target.get('maxPlayers', 44)
            owner = target.get('ownerName', 'medo230y')

            embed = discord.Embed(title="🛡️ ABR BORDER ROLEPLAY 🇺🇸", color=0x2ecc71)
            embed.description = ">>> **Welcome to the Border.**\n*Serious Roleplay & Community Events*"
            
            # Fields formatted for better alignment
            embed.add_field(name="📶 Server Status", value="🟢 `Active`", inline=True)
            embed.add_field(name="👥 Population", value=f"`{players} / {max_p}`", inline=True)
            embed.add_field(name="👑 Community Owner", value=f"`{owner}`", inline=True)
            embed.add_field(name="🔑 Private Code", value=f"`{JOIN_CODE}`", inline=False)
            embed.add_field(name="🕒 Real-Time Sync", value=f"Updated <t:{int(time.time())}:R>", inline=False)
            
            # Use a working icon for the footer
            embed.set_footer(text="Bot made for ABR • Developed by Youssef", icon_url="https://cdn-icons-png.flaticon.com/512/6840/6840478.png")

            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(MESSAGE_ID)
            await msg.edit(content=None, embed=embed, view=JoinButton(JOIN_CODE))
            print("✅ Fixed and Updated!")
    except Exception as e:
        print(f"🔥 Error: {e}")
    
    await bot.close()

bot.run(TOKEN)
