import discord
from discord import app_commands
import asyncio
import threading
from flask import Flask
import os
import random
from dotenv import load_dotenv
from obfuscator import SttarObfuscator

load_dotenv()

# Flask Web Server (for Render uptime)
app = Flask(__name__)

@app.route('/')
def home():
    return "Sttar Obfuscator is running! ✨"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

# Discord Bot
intents = discord.Intents.default()
intents.message_content = False
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

obfuscator = SttarObfuscator()

@client.event
async def on_ready():
    await tree.sync()
    print(f"Sttar Obfuscator is online as {client.user}")

@tree.command(name="obfuscate", description="Obfuscate Lua/Luau code with Sttar Custom VM")
@app_commands.describe(
    code="The Lua/Luau script to obfuscate",
    intensity="Protection level"
)
@app_commands.choices(intensity=[
    app_commands.Choice(name="Extreme", value="Extreme"),
    app_commands.Choice(name="Medium", value="Medium")
])
async def obfuscate(interaction: discord.Interaction, code: str, intensity: str = "Extreme"):
    await interaction.response.defer()

    # Flashy Loading Embed
    loading_embed = discord.Embed(
        title="🔄 **OBFUSCATING YOUR CODE...**",
        description="```Please wait while our custom VM protection kicks in... ✨```",
        color=0xC026D3  # Neon Purple/Pink
    )
    loading_embed.set_footer(text="Sttar Obfuscator • Powered by Custom VM")
    loading_embed.timestamp = discord.utils.utcnow()
    await interaction.followup.send(embed=loading_embed)

    try:
        obfuscated_code, stats = obfuscator.obfuscate(code, intensity)
        
        rand_num = random.randint(100000, 999999)
        filename = f"Sttar_Obfuscator_{rand_num}.lua"
        
        # Success Embed
        success_embed = discord.Embed(
            title="✅ **OBFUSCATE SUCCESS!** ✨",
            description="Your code is now protected with **Sttar Custom VM**",
            color=0x22C55E  # Neon Green
        )
        success_embed.add_field(name="📏 Original Size", value=f"`{stats['original']:,}` chars", inline=True)
        success_embed.add_field(name="📏 Obfuscated Size", value=f"`{stats['obfuscated']:,}` chars", inline=True)
        success_embed.add_field(name="⚡ Compression", value=f"`{stats['compression']}%`", inline=True)
        success_embed.add_field(name="🛡️ Protection Level", value="**Custom VM + Heavy Obfuscation**", inline=False)
        success_embed.set_footer(text=f"Sttar Obfuscator • Secured • {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M')}")
        success_embed.timestamp = discord.utils.utcnow()

        # Send file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)
        
        await interaction.followup.send(embed=success_embed, file=discord.File(filename))
        
        # Cleanup
        os.remove(filename)

    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Obfuscation Failed",
            description=f"```Error: {str(e)}```",
            color=0xEF4444
        )
        await interaction.followup.send(embed=error_embed)

# Run Flask in thread
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Main
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("DISCORD_TOKEN not found in .env")
    else:
        client.run(TOKEN)
