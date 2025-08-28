import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from commands import register_commands, register_help_command, register_character_specific_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

register_help_command(bot)
register_character_specific_commands(bot)
register_commands(bot, "killer")
register_commands(bot, "survivor")

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)

