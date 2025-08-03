import discord
from discord.ext import commands
from funcs.randomize_funcs import get_random_perks
from funcs.data_funcs import map_perks

class RandomizeView(discord.ui.View):
    def __init__(self, ctx, perks_list, random_result, exclude_ids):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.perks_list = perks_list
        self.exclude_ids = exclude_ids
        self.random_perks = random_result
        self.selected_ids = []

        options = [
            discord.SelectOption(
                label=f'{perk["perk_data"]["name"]}', 
                value=str(perk["perk_data"]["id"])
            )
            for perk in random_result
        ]

        self.select = discord.ui.Select(
            placeholder="Choose perks to replace",
            min_values=0,
            max_values=4,
            options=options
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

        replace_btn = discord.ui.Button(label="Replace Selected Perks", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.handle_replace
        self.add_item(replace_btn)

    async def handle_select(self, interaction: discord.Interaction):
        self.selected_ids = [int(value) for value in self.select.values]
        await interaction.response.defer()
    
    async def handle_replace(self, interaction: discord.Interaction):
        for item in self.random_perks:
            item["replace"] = item["perk_data"]["id"] in self.selected_ids

        randomize_result = get_random_perks(
            self.perks_list, 
            self.random_perks, 
            self.exclude_ids
        )

        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_perks = randomize_result["random_perks"]

        msg = "\n".join(
            [f'→ **{perk["perk_data"]["name"]}** from *{perk["perk_data"]["owner_name"]}*' for perk in self.random_perks]
        )

        self.select.options = [
            discord.SelectOption(
                label=f'{perk["perk_data"]["name"]}', 
                value=str(perk["perk_data"]['id'])
            ) for perk in self.random_perks
        ]

        content = f"**{self.ctx.author.mention}**, here are your new perks:\n \n{msg} \n \n If you don't own any of these perks, you can replace them!\n \n"

        await interaction.response.edit_message(content=content, view=self)



