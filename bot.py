import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import random
import time
from io import BytesIO
from datetime import datetime
from flask import Flask
from threading import Thread
from obfuscator import process_code

# --- Flask Web Server Setup ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Sttar Obfuscator is running!"

def run_flask():
    # Use the port Render assigns (default 10000)
    port = int(os.environ.get("PORT", 10000))
    # Disable reloader to avoid thread issues, enable threading for concurrency
    app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()

# --- Discord Bot Setup ---
class SttarBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        await self.tree.sync()
        print("Bot is ready and slash commands are synced.")

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
    # 1. Send Flashy Loading Embed
    loading_embed = discord.Embed(
        title="🔄 **OBFUSCATING YOUR CODE...**",
        description="`Please wait while our custom protection layers kick in... ✨`",
        color=0xFF00FF  # Neon Purple/Pink
    )
    loading_embed.set_footer(text="Sttar Obfuscator")
    loading_embed.timestamp = discord.utils.utcnow()
    
    await interaction.response.send_message(embed=loading_embed)
    
    # Simulate processing delay to mimic complex compilation
    await asyncio.sleep(2)
    
    original_size = len(code)
    level_value = intensity.value if intensity else "extreme"
    level_name = intensity.name if intensity else "Extreme - Max Obfuscation & Junk Insertion"

    try:
        # Process the code using our custom logic
        obfuscated_code = process_code(code, intensity=level_value)
        new_size = len(obfuscated_code)
        
        # Calculate size expansion percentage (avoid division by zero)
        if original_size > 0:
            change = round(((new_size - original_size) / original_size) * 100, 1)
            change_str = f"+{change}%" if change > 0 else f"{change}%"
        else:
            change_str = "N/A"

        # Create a clean file object in memory
        file_bytes = BytesIO(obfuscated_code.encode('utf-8'))
        random_id = random.randint(100000, 999999)
        filename = f"Sttar_Obfuscator_{random_id}.lua"
        discord_file = discord.File(fp=file_bytes, filename=filename)

        # 2. Send Flashy Success Embed
        success_embed = discord.Embed(
            title="✅ **OBFUSCATION SUCCESSFUL!** ✨",
            description="Your script has been wrapped and scrambled securely.",
            color=0x00FF00  # Neon Green
        )
        success_embed.add_field(name="📝 Original Size", value=f"`{original_size} characters`", inline=True)
        success_embed.add_field(name="🔒 Obfuscated Size", value=f"`{new_size} characters`", inline=True)
        success_embed.add_field(name="📊 Code Expansion", value=f"`{change_str}`", inline=True)
        success_embed.add_field(name="🛡️ Protection Profile", value=f"`{level_name}`", inline=False)
        success_embed.add_field(name="🎮 Executor Compatibility", value="`Fully compatible with Lua 5.1 / Luau executors`", inline=False)
        
        success_embed.set_footer(text="Sttar Obfuscator • Secured and Encrypted")
        success_embed.timestamp = discord.utils.utcnow()

        # Update the initial message with results and attach the script
        await interaction.edit_original_response(embed=success_embed, attachments=[discord_file])

    except Exception as e:
        error_embed = discord.Embed(
            title="❌ **PROCESS ERROR**",
            description=f"An error occurred while processing: `{str(e)}`",
            color=0xFF0000
        )
        await interaction.edit_original_response(embed=error_embed)

if __name__ == "__main__":
    # Start the Flask web server in a background thread
    keep_alive()
    
    # Give Flask a moment to bind to the port before Render scans
    time.sleep(2)
    
    # Start the Discord bot
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("CRITICAL ERROR: Environment variable 'DISCORD_BOT_TOKEN' is empty or missing.")
    else:
        bot.run(TOKEN)
