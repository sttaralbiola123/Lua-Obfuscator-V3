import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import random
from io import BytesIO
from datetime import datetime
from flask import Flask
from threading import Thread
from obfuscator import process_code

# -------------------- FLASK WEB SERVER (for Render keep-alive) --------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Sttar Obfuscator is running!"

def run_flask():
    # Use Render's assigned port or default to 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# -------------------- DISCORD BOT SETUP --------------------
class SttarBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True   # optional, for future commands
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Bot is ready and slash commands are synced.")

bot = SttarBot()

@bot.tree.command(name="obfuscate", description="Obfuscate your Lua/Luau script for Roblox executors.")
@app_commands.describe(
    code="The Lua script you want to obfuscate",
    intensity="Select the level of visual complexity and junk generation"
)
@app_commands.choices(intensity=[
    app_commands.Choice(name="Low - Basic Hex Scrambling", value="low"),
    app_commands.Choice(name="Medium - Hex + Variable Mangling", value="medium"),
    app_commands.Choice(name="Extreme - Max Obfuscation & Junk Insertion", value="extreme"),
])
async def obfuscate(interaction: discord.Interaction, code: str, intensity: app_commands.Choice[str] = None):
    # Send a "processing" embed
    loading_embed = discord.Embed(
        title="🔄 **OBFUSCATING YOUR CODE...**",
        description="`Please wait while our custom protection layers are applied... ✨`",
        color=0xFF00FF  # Neon purple
    )
    loading_embed.set_footer(text="Sttar Obfuscator")
    loading_embed.timestamp = discord.utils.utcnow()
    
    await interaction.response.send_message(embed=loading_embed)
    
    # Small delay to simulate work (optional)
    await asyncio.sleep(1)
    
    original_size = len(code)
    level_value = intensity.value if intensity else "extreme"
    level_name = intensity.name if intensity else "Extreme - Max Obfuscation & Junk Insertion"

    try:
        # Call the obfuscator engine
        obfuscated_code = process_code(code, intensity=level_value)
        new_size = len(obfuscated_code)
        
        # Calculate size change percentage
        if original_size > 0:
            change = round(((new_size - original_size) / original_size) * 100, 1)
        else:
            change = 0.0
        change_str = f"+{change}%" if change > 0 else f"{change}%"

        # Prepare file for upload
        file_bytes = BytesIO(obfuscated_code.encode('utf-8'))
        random_id = random.randint(100000, 999999)
        filename = f"Sttar_Obfuscator_{random_id}.lua"
        discord_file = discord.File(fp=file_bytes, filename=filename)

        # Success embed
        success_embed = discord.Embed(
            title="✅ **OBFUSCATION SUCCESSFUL!** ✨",
            description="Your script has been securely wrapped and scrambled.",
            color=0x00FF00  # Neon green
        )
        success_embed.add_field(name="📝 Original Size", value=f"`{original_size} characters`", inline=True)
        success_embed.add_field(name="🔒 Obfuscated Size", value=f"`{new_size} characters`", inline=True)
        success_embed.add_field(name="📊 Code Expansion", value=f"`{change_str}`", inline=True)
        success_embed.add_field(name="🛡️ Protection Profile", value=f"`{level_name}`", inline=False)
        success_embed.add_field(name="🎮 Executor Compatibility", value="`Fully compatible with Lua 5.1 / Luau executors`", inline=False)
        success_embed.set_footer(text="Sttar Obfuscator • Secured & Encrypted")
        success_embed.timestamp = discord.utils.utcnow()

        # Edit the original response with the result and attach the file
        await interaction.edit_original_response(embed=success_embed, attachments=[discord_file])

    except Exception as e:
        # FIXED: Unterminated f-string → used triple quotes for multi-line
        error_embed = discord.Embed(
            title="❌ **PROCESS ERROR**",
            description=f"""An error occurred while processing your request:
`{str(e)}`

Please check your script and try again.""",
            color=0xFF0000
        )
        await interaction.edit_original_response(embed=error_embed)

# -------------------- STARTUP --------------------
if __name__ == "__main__":
    keep_alive()  # Start the Flask server in a background thread
    
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("CRITICAL ERROR: Environment variable 'DISCORD_BOT_TOKEN' is missing.")
    else:
        bot.run(TOKEN)
