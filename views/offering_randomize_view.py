import discord
from core.randomize_funcs import get_random_offering
from views.final_setup_view import FinalSetupView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class OfferingRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = True):

        followup = {
            "killer": {"view": FinalSetupView, "next_drawn": "summary"},
            "survivor": {"view": FinalSetupView, "next_drawn": "summary"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )
        
        offerings = data_loader.offerings_list
        self.offerings_list = offerings[f"{character_type}_offerings"]
        self.random_offering = None
        self.exclude_ids = []

        self.randomize()

        replace_btn = discord.ui.Button(label="Replace Offering", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace
        self.add_item(replace_btn)
    
    def get_message(self):
        msg =  f'→ **{self.random_offering["offering_name"]}** of *{self.random_offering["offering_rarity"]}* rarity'

        return f'**{self.ctx.author.mention}**, you will play with: \n \n{msg} ! \n \n If you don\'t own it, you can replace it\n \n'
            
    def randomize(self):
        randomize_result = get_random_offering(
            self.offerings_list,
            self.exclude_ids,
            self.random_offering
        )
        
        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_offering = randomize_result[f"random_offering"]
        
    async def accept(self, interaction: discord.Interaction):
        self.state.offering = self.random_offering
        next_view = self.followup_view["view"](ctx=self.ctx, state=self.state, character_type=self.character_type)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )

