import os
import discord
import requests
from discord.ext import commands
import time
import asyncio

# --- CONFIGURATION (GITHUB SECRETS) ---
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
MESSAGE_ID = int(os.environ['DISCORD_MESSAGE_ID'])
MY_SERVER_ID = "4606-8ef3-aa7adcbe59bc" 
JOIN_CODE = "iz99bb68"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- PROFESSIONAL UI: JOIN BUTTON ---
class JoinButton(discord.ui.View):
    def __init__(self, join_code):
        super().__init__()
        # Direct link to launch Roblox and join the private server
        url = f"https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode%3D{join_code}"
        self.add_item(discord.ui.Button(
            label='Join Server', 
            url=url, 
            emoji='🎮', 
            style=discord.ButtonStyle.link
        ))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}. Updating ABR Status...")
    try:
        # 1. Fetch Roblox Data
        response = requests.get("https://api.emergency-hamburg.com/public/servers", timeout=10)
        all_servers = response.json()
        target = next((s for s in all_servers if MY_SERVER_ID in s.get('privateServerId', '')), None)
                
        if target:
            players = target.get('currentPlayers', 0)
            max_p = target.get('maxPlayers', 44)
            owner = target.get('ownerName', 'medo230y')
            owner_id = target.get('ownerId', '1')

            # 2. Build the Professional Embed
            embed = discord.Embed(
                title="🛡️ ABR BORDER ROLEPLAY 🇺🇸", 
                description=">>> **Welcome to the Border.** \n*Serious Roleplay & Community Events*",
                color=0x2ecc71 # Emerald Green
            )
            
            # Row 1
            embed.add_field(name="📶 Server Status", value="🟢 `Active`", inline=True)
            embed.add_field(name="👥 Population", value=f"```css\n{players} / {max_p}\n```", inline=True)
            
            # Row 2
            embed.add_field(name="👑 Community Owner", value=f"[{owner}](https://www.roblox.com/users/{owner_id}/profile)", inline=True)
            embed.add_field(name="🔑 Private Code", value=f"`{JOIN_CODE}`", inline=True)
            
            # Row 3 (Full Width)
            sync_time = int(time.time())
            embed.add_field(name="🕒 Real-Time Sync", value=f"Updated <t:{sync_time}:R>", inline=False)
            
            # Visuals
            embed.set_thumbnail(url="https://i.imgur.com/8E89XG1.png") 

            # YOUR NEW FOOTER
            embed.set_footer(
                text="Bot made for ABR • Developed by Youssef", 
                icon_url="https://cdn-icons-png.flaticon.com/512/6840/6840478.png"
            )

            # 3. Update Discord Message
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                msg = await channel.fetch_message(MESSAGE_ID)
                await msg.edit(content=None, embed=embed, view=JoinButton(JOIN_CODE))
                print("✅ Update Successful!")
        else:
            print("❌ Server not found.")
            
    except Exception as e:
        print(f"🔥 Error: {e}")
    
    await bot.close()

bot.run(TOKEN)
