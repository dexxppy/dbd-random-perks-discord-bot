import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from commands import register_commands, register_help_command, register_character_specific_commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_guild_join(guild):
    log_message = ""
    try:
        owner = guild.get_member(guild.owner_id)
        if owner is None:
            owner = await guild.fetch_member(guild.owner_id)

        log_message = f"Bot invited to {guild.name} (ID: {guild.id}) by {owner}"
    except Exception as e:
        log_message = f"Error inviting to new server: {e}"
    finally:
        print(log_message)
        with open("bot_logs.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

register_help_command(bot)
register_character_specific_commands(bot)
register_commands(bot, "killer")
register_commands(bot, "survivor")

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)

