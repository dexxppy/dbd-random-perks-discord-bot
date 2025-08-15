import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from funcs.randomize_funcs import get_random_perks
from views.PerksRandomizeView import PerksRandomizeView
from views.CharacterRandomizeView import CharacterRandomizeView
from utils.DataLoader import DataLoader
from utils.SetupState import SetupState


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
        
# @bot.command()
# async def random_killer(ctx):
#     character_type = "killer"
#     data_loader = DataLoader(character_type)
#     perks_list = data_loader.perks_list
    
#     randomize_result = get_random_perks(perks_list, [], character_type)
#     exclude_ids = randomize_result["exclude_ids"]
#     random_perks = randomize_result["random_perks"]

#     perks_msg = "\n".join(
#         [f'→ **{perk["perk_data"]["killer_perk_name"]}** from *{perk["perk_data"]["killer_owner_name"]}*' for perk in random_perks]
#     )

#     msg = f"**{ctx.author.mention}**, here are your random killer perks:\n \n{perks_msg} \n \n If you don't own any of these perks, you can replace them!\n \n"
#     view = PerksRandomizeView(ctx, character_type, perks_list, random_perks, exclude_ids)
#     await ctx.send(msg, view=view)

# @bot.command()
# async def random_surv(ctx):
#     character_type = "survivor"
#     data_loader = DataLoader(character_type)
#     perks_list = data_loader.perks_list
    
#     randomize_result = get_random_perks(perks_list, [], character_type)
#     exclude_ids = randomize_result["exclude_ids"]
#     random_perks = randomize_result["random_perks"]

#     perks_msg = "\n".join(
#         [f'→ **{perk["perk_data"]["survivor_perk_name"]}** from *{perk["perk_data"]["survivor_owner_name"]}*' for perk in random_perks]
#     )

#     msg = f"**{ctx.author.mention}**, here are your random survivor perks:\n \n{perks_msg} \n \n If you don't own any of these perks, you can replace them!\n \n"
#     view = PerksRandomizeView(ctx, character_type, perks_list, random_perks, exclude_ids)
#     await ctx.send(msg, view=view)

@bot.command()
async def surv_setup(ctx):
    data_loader = DataLoader("survivor")
    state = SetupState(ctx.author.id)
    view = CharacterRandomizeView(ctx=ctx, data_loader=data_loader, state=state, character_type="survivor")

    await ctx.send(
        content=view.get_message(),
        view=view
    )

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)

