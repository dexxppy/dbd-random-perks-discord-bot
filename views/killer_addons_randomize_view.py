import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_killer_addons_set
from views.offering_randomize_view import OfferingRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState

class KillerAddonsRandomizeView(discord.ui.View):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, next_step: bool = False):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.data_loader = data_loader
        self.state = state
        
        self.character_type = "killer"
        
        self.addons_list = self.state.character["killer_addons"]
        self.next_step = next_step

        self.random_addons_set = []
        self.exclude_ids = []
        self.selected_ids = []
        
        self.followup_view = {
            "view": OfferingRandomizeView,
            "next_drawn": "offering"
        }
        
        self.randomize_addons_set()
        
        self.select = discord.ui.Select(
            placeholder="Choose addons to replace",
            min_values=1,
            max_values=2,
            options=get_options_for_select(self.random_addons_set, "addon", self.character_type)
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

        replace_btn = discord.ui.Button(label="Replace Selected Addons", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace_addons
        self.add_item(replace_btn)
        
        if self.next_step:
            btn_accept = discord.ui.Button(label=f'Continue with {self.followup_view["next_drawn"]} ➡', style=discord.ButtonStyle.success)
            btn_accept.callback = self.accept_addons
            self.add_item(btn_accept)
            
    def get_message(self):
        msg = "\n".join(
            [
                "Addons:",
                *[
                    f'→ **{addon["addon_data"]["killer_addon_name"]}** of *{addon["addon_data"]["killer_addon_rarity"]}* rarity'
                    for addon in self.random_addons_set
                ]
            ]
        )

        return f'**{self.ctx.author.mention}**, this is your addons set:\n \n{msg} \n \n If you don\'t own any of these addons, you can replace it!\n \n'
                
    def randomize_addons_set(self):
        randomize_result = get_random_killer_addons_set(
            all_addons_list=self.addons_list,
            initial_addons_list=self.random_addons_set,
            exclude_ids=self.exclude_ids
        )
        
        self.random_addons_set = randomize_result["random_addons"]
        self.exclude_ids = randomize_result["exclude_ids"]
        
    async def handle_select(self, interaction: discord.Interaction):
        self.selected_ids = [int(value) for value in self.select.values]
        await interaction.response.defer()
        
    async def replace_addons(self, interaction: discord.Interaction):
        for item in self.random_addons_set:
            item["replace"] = item["addon_data"][f"{self.character_type}_addon_id"] in self.selected_ids
            
        self.randomize_addons_set()
        self.select.options = get_options_for_select(self.random_addons_set, "addon", self.character_type)

        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)

    async def accept_addons(self, interaction: discord.Interaction):
        self.state.killer_addons = self.random_addons_set
        next_view = self.followup_view["view"](ctx=self.ctx, 
                                               data_loader=self.data_loader, 
                                               state=self.state, 
                                               character_type=self.character_type, 
                                               next_step=True)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )
        

