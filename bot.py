import os
import discord
import requests
from discord.ext import commands
from datetime import datetime

# --- CONFIGURATION ---
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
MESSAGE_ID = int(os.environ['DISCORD_MESSAGE_ID'])
MY_SERVER_ID = "4606-8ef3-aa7adcbe59bc" 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# This creates the "Join Server" button
class JoinButton(discord.ui.View):
    def __init__(self, join_code):
        super().__init__()
        # Official Roblox protocol to launch the game with the join code
        url = f"https://www.roblox.com/games/start?placeId=3334450855&launchData={join_code}"
        self.add_item(discord.ui.Button(label='Join Server', url=url, emoji='🔗', style=discord.ButtonStyle.link))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        response = requests.get("https://api.emergency-hamburg.com/public/servers")
        all_servers = response.json()
        
        target = next((s for s in all_servers if MY_SERVER_ID in s.get('privateServerId', '')), None)
                
        if target:
            players = target.get('currentPlayers', 0)
            max_p = target.get('maxPlayers', 44)
            owner = target.get('ownerName', 'medo230y')
            code = target.get('code', 'TBm2HgcGtf')

            embed = discord.Embed(title="🚨 BORDER RP 🚧 🇺🇸", color=0x2ecc71)
            embed.add_field(name="📶 Status", value="🟢 Online", inline=False)
            embed.add_field(name="🎮 Players", value=f"`{players} / {max_p}`", inline=True)
            embed.add_field(name="👑 Owner", value=f"[{owner}](https://www.roblox.com/users/{target.get('ownerId')}/profile)", inline=True)
            embed.add_field(name="🔗 Server Code", value=f"`{code}`", inline=False)
            
            avatar_url = target.get('ownerProfileUrl', '')
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)

            embed.set_footer(text=f"Last updated: {datetime.now().strftime('%I:%M %p')}")

            channel = bot.get_channel(CHANNEL_ID)
            if channel is None:
                print("Error: Could not find channel. Check DISCORD_CHANNEL_ID.")
                return

            msg = await channel.fetch_message(MESSAGE_ID)
            
            # Edit the message with the new design
            await msg.edit(content=None, embed=embed, view=JoinButton(code))
            print("Successfully updated Discord!")
        else:
            print("Server not found in API. It might be offline.")
            
    except Exception as e:
        print(f"Error: {e}")
    
    await bot.close()

bot.run(TOKEN)

bot.run(TOKEN)
