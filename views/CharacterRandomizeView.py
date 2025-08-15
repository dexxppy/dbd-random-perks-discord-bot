import discord
from discord.ext import commands
from funcs.randomize_funcs import get_random_character
from views.PerksRandomizeView import PerksRandomizeView
from utils.DataLoader import DataLoader
from utils.SetupState import SetupState

class CharacterRandomizeView(discord.ui.View):

    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type, next_step: bool = True):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.data_loader = data_loader
        self.state = state
        
        self.character_type = character_type
        self.characters_list = data_loader.characters_list
        self.next_step = next_step

        self.random_character = None
        self.exclude_ids = []
                
        self.followup_view = {
            "killer": {"view": PerksRandomizeView, "next_drawn": "perks"},
            "survivor": {"view": PerksRandomizeView, "next_drawn": "perks"}
        }.get(self.character_type)
        
        self.randomize_character()

        replace_btn = discord.ui.Button(label="Replace Character", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace_character
        self.add_item(replace_btn)
        
        if self.next_step:
            btn_accept = discord.ui.Button(label=f'Continue with {self.followup_view["next_drawn"]} ➡', style=discord.ButtonStyle.success)
            btn_accept.callback = self.accept_character
            self.add_item(btn_accept)
    
    def get_message(self):
        return f'**{self.ctx.author.mention}**, you will play as: \n \n**{self.random_character[f"{self.character_type}_name"]}** ! \n \n If you don\'t own it, you can replace it\n \n'
            
    def randomize_character(self):
        randomize_result = get_random_character(
            self.characters_list,
            self.character_type,
            self.exclude_ids,
            self.random_character
        )
        
        self.exclude_ids = randomize_result["exclude_ids"]
        self.random_character = randomize_result[f"random_{self.character_type}"]
    
    async def replace_character(self, interaction: discord.Interaction):
        
        self.randomize_character()
        content = self.get_message()

        await interaction.response.edit_message(content=content, view=self)
        
    async def accept_character(self, interaction: discord.Interaction):
        self.state.character = self.random_character
        next_view = self.followup_view["view"](ctx=self.ctx, data_loader=self.data_loader, state=self.state, character_type=self.character_type, next_step=True)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )


