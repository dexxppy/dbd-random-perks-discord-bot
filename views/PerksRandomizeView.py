import discord
from utils.views_utils import get_options_for_select
from discord.ext import commands
from funcs.randomize_funcs import get_random_perks
from views.FinalSetupView import FinalSetupView
from utils.DataLoader import DataLoader
from utils.SetupState import SetupState

class PerksRandomizeView(discord.ui.View):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = False):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.data_loader = data_loader
        self.state = state
        
        self.character_type = character_type
        self.perks_list = data_loader.perks_list
        self.next_step = next_step

        self.random_perks = []
        self.exclude_ids = []
        self.selected_ids = []

        self.followup_view = {
            "killer": {"view": FinalSetupView, "next_drawn": "summary"},
            "survivor": {"view": FinalSetupView, "next_drawn": "summary"}
        }.get(self.character_type)
        
        self.randomize_perks()

        self.select = discord.ui.Select(
            placeholder="Choose perks to replace",
            min_values=0,
            max_values=4,
            options=get_options_for_select(self.random_perks, "perk", character_type)
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

        replace_btn = discord.ui.Button(label="Replace Selected Perks", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace_perks
        self.add_item(replace_btn)
        
        if self.next_step:
            btn_accept = discord.ui.Button(label=f'Continue with {self.followup_view["next_drawn"]} ➡', style=discord.ButtonStyle.success)
            btn_accept.callback = self.accept_perks
            self.add_item(btn_accept)
            
    def get_message(self):
        msg = "\n".join(
            [f'→ **{ perk["perk_data"][f"{self.character_type}_perk_name"]}** from *{perk["perk_data"][f"{self.character_type}_owner_name"]}*'
            for perk in self.random_perks]
        )

        return f'**{self.ctx.author.mention}**, these are your perks:\n \n{msg} \n \n If you don\'t own any of these perks, you can replace them!\n \n'
            
    def randomize_perks(self):
        randomize_result = get_random_perks(
            self.perks_list, 
            self.random_perks, 
            self.character_type,
            self.exclude_ids
        )

        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_perks = randomize_result["random_perks"]
        
    async def handle_select(self, interaction: discord.Interaction):
        self.selected_ids = [int(value) for value in self.select.values]
        await interaction.response.defer()
    
    async def replace_perks(self, interaction: discord.Interaction):
        for item in self.random_perks:
            item["replace"] = item["perk_data"][f"{self.character_type}_perk_id"] in self.selected_ids

        self.randomize_perks()
        self.select.options = get_options_for_select(self.random_perks, "perk", self.character_type)

        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)

    async def accept_perks(self, interaction: discord.Interaction):
        self.state.perks = self.random_perks
        next_view = self.followup_view["view"](ctx=self.ctx, state=self.state)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )

