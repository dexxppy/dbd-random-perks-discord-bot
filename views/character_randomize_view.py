import discord
from core.randomize_funcs import get_random_character
from views.offering_randomize_view import OfferingRandomizeView
from views.perks_randomize_view import PerksRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class CharacterRandomizeView(BaseRandomizeView):

    def __init__(self, ctx, data_loader, state, character_type, next_step: bool = True):

        followup = {
            "killer": {"view": PerksRandomizeView, "next_drawn": "perks"},
            "survivor": {"view": PerksRandomizeView, "next_drawn": "perks"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )

        self.characters_list = data_loader.characters_list
        self.random_character = None
        self.exclude_ids = []

        self.randomize()

        replace_btn = discord.ui.Button(label="Replace Character", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace
        self.add_item(replace_btn)
    
    def get_message(self):
        return f'**{self.ctx.author.mention}**, you will play as: \n \n**{self.random_character[f"{self.character_type}_name"]}** ! \n \n If you don\'t own it, you can replace it\n \n'
            
    def randomize(self):
        randomize_result = get_random_character(
            self.characters_list,
            self.character_type,
            self.exclude_ids,
            self.random_character
        )
        
        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_character = randomize_result[f"random_{self.character_type}"]
        
    async def accept(self, interaction: discord.Interaction):
        self.state.character = self.random_character
        next_view = self.followup_view["view"](ctx=self.ctx, 
                                               data_loader=self.data_loader, 
                                               state=self.state, 
                                               character_type=self.character_type, 
                                               next_step=True)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )


