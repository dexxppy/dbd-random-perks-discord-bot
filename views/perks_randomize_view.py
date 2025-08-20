import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_perks
from views.item_randomize_view import ItemRandomizeView
from views.killer_addons_randomize_view import KillerAddonsRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.offering_randomize_view import OfferingRandomizeView
from views.randomize_view import BaseRandomizeView


class PerksRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = False):

        # followup = {
        #     "killer": {"view": KillerAddonsRandomizeView, "next_drawn": "addons"},
        #     "survivor": {"view": ItemRandomizeView, "next_drawn": "item"}
        # }


        followup = {
            "killer": {"view": OfferingRandomizeView, "next_drawn": "perks"},
            "survivor": {"view": ItemRandomizeView, "next_drawn": "item"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )
        
        self.perks_list = data_loader.perks_list

        self.random_perks = []
        self.exclude_ids = []

        self.randomize()

        self.select = discord.ui.Select(
            placeholder="Choose perks to replace",
            min_values=1,
            max_values=4,
            options=get_options_for_select(self.random_perks, "perk", character_type)
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

        replace_btn = discord.ui.Button(label="Replace Selected Perks", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace
        self.add_item(replace_btn)
            
    def get_message(self):
        msg = "\n".join(
            [f'→ **{ perk["perk_data"][f"{self.character_type}_perk_name"]}** from *{perk["perk_data"][f"{self.character_type}_owner_name"]}*'
            for perk in self.random_perks]
        )

        return f'**{self.ctx.author.mention}**, these are your perks:\n \n{msg} \n \n If you don\'t own any of these perks, you can replace them!\n \n'
            
    def randomize(self):
        randomize_result = get_random_perks(
            self.perks_list, 
            self.random_perks, 
            self.character_type,
            self.exclude_ids
        )

        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_perks = randomize_result["random_perks"]
    
    async def replace(self, interaction: discord.Interaction):
        for item in self.random_perks:
            item["replace"] = item["perk_data"][f"{self.character_type}_perk_id"] in self.selected_ids

        self.randomize()
        self.select.options = get_options_for_select(self.random_perks, "perk", self.character_type)

        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)

    async def accept(self, interaction: discord.Interaction):
        self.state.perks = self.random_perks
        next_view = self.followup_view["view"](ctx=self.ctx,
                                               data_loader=self.data_loader,
                                               state=self.state,
                                               next_step=True)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )

