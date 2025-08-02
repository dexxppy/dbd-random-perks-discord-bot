import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from funcs.randomize_funcs import get_random_perks
from funcs.data_funcs import map_perks
from funcs.RandomizeView import RandomizeView

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
        
@bot.command()
async def random_killer(ctx):
    perks_list = map_perks('killers', 'killer_perks', 'killer_id')
    randomize_result = get_random_perks(perks_list, [])
    exclude_ids = randomize_result["exclude_ids"]
    random_perks = randomize_result["random_perks"]

    perks_msg = "\n".join(
        [f'→ **{perk["perk_data"]["name"]}** from *{perk["perk_data"]["owner_name"]}*' for perk in random_perks]
    )

    msg = f"**{ctx.author.mention}**, here are your random killer perks:\n \n{perks_msg} \n \n If you don't own any of these perks, you can replace them!\n \n"
    view = RandomizeView(ctx, perks_list, random_perks, exclude_ids)
    await ctx.send(msg, view=view)

@bot.command()
async def random_surv(ctx):
    perks_list = map_perks('survivors', 'survivor_perks', 'survivor_id')
    randomize_result = get_random_perks(perks_list, [])
    exclude_ids = randomize_result["exclude_ids"]
    random_perks = randomize_result["random_perks"]

    perks_msg = "\n".join(
        [f'→ **{perk["perk_data"]["name"]}** from *{perk["perk_data"]["owner_name"]}*' for perk in random_perks]
    )

    msg = f"**{ctx.author.mention}**, here are your random survivor perks:\n \n{perks_msg} \n \n If you don't own any of these perks, you can replace them!\n \n"
    view = RandomizeView(ctx,perks_list, random_perks, exclude_ids)
    await ctx.send(msg, view=view)

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
