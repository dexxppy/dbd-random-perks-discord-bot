import discord
from utils.views_utils import get_options_for_select
from core.randomize_funcs import get_random_item_addons_set, get_random_item_with_addons
from views.offering_randomize_view import OfferingRandomizeView
from core.data_loader import DataLoader
from core.state import SetupState
from views.randomize_view import BaseRandomizeView


class ItemRandomizeView(BaseRandomizeView):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, next_step: bool = False):

        character_type = "survivor"

        followup = {
            "killer": {"view": OfferingRandomizeView, "next_drawn": "offering"},
            "survivor": {"view": OfferingRandomizeView, "next_drawn": "offering"}
        }

        super().__init__(
            ctx, data_loader, state, character_type, next_step, followup_view=followup
        )

        items_data = self.data_loader.items_list
        self.items_list = items_data["items"]
        self.addons_list = items_data["addons"]

        self.random_item_set = None
        self.exclude_ids_items = []
        self.exclude_ids_addons = []

        self.randomize()
        
        self.replace_item_button = discord.ui.Button(label="Replace Item", style=discord.ButtonStyle.primary)
        self.replace_item_button.callback = self.replace_item
        self.add_item(self.replace_item_button)
        
        self.select = discord.ui.Select(
            placeholder="Choose addons to replace",
            min_values=1,
            max_values=2,
            options=get_options_for_select(self.random_item_set["addons"], "addon", self.character_type)
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

        replace_btn = discord.ui.Button(label="Replace Selected Addons", style=discord.ButtonStyle.primary)
        replace_btn.callback = self.replace_addons
        self.add_item(replace_btn)
            
    def get_message(self):
        msg = "\n".join(
            [
                "Item:",
                f'→ **{self.random_item_set["item"]["survivor_item_name"]}** of *{self.random_item_set["item"]["survivor_item_rarity"]}* rarity',
                "With Addons:",
                *[
                    f'→ **{addon["addon_data"]["survivor_addon_name"]}** of *{addon["addon_data"]["survivor_addon_rarity"]}* rarity'
                    for addon in self.random_item_set["addons"]
                ]
            ]
        )

        return f'**{self.ctx.author.mention}**, this is your item set:\n \n{msg} \n \n If you don\'t own any of these objects, you can replace it!\n \n'
            
    def randomize(self):
        randomize_result = get_random_item_with_addons(
            all_items_list=self.items_list,
            all_addons_list=self.addons_list,
            exclude_ids_item=self.exclude_ids_items,
            exclude_ids_addons=self.exclude_ids_addons,
            last_drawn_item_with_addons=self.random_item_set
        )

        self.random_item_set = randomize_result["random_item_set"]
        self.exclude_ids_items = randomize_result["exclude_ids_item"]
        self.exclude_ids_addons = randomize_result["exclude_ids_addons"]
                
    def randomize_items_addons_set(self):
        randomize_result = get_random_item_addons_set(
            all_addons_list=self.addons_list,
            initial_addons_list=self.random_item_set["addons"],
            item_family_name=self.random_item_set["item"]["survivor_item_family"],
            exclude_ids=self.exclude_ids_addons
        )
        
        self.random_item_set["addons"] = randomize_result["random_addons"]
        self.exclude_ids_addons = randomize_result["exclude_ids"]

    
    async def replace_item(self, interaction: discord.Interaction):
        self.randomize()
        self.select.options = get_options_for_select(self.random_item_set["addons"], "addon", self.character_type)

        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)
        
    async def replace_addons(self, interaction: discord.Interaction):
        for item in self.random_item_set["addons"]:
            item["replace"] = item["addon_data"][f"{self.character_type}_addon_id"] in self.selected_ids
            
        self.randomize_items_addons_set()
        self.select.options = get_options_for_select(self.random_item_set["addons"], "addon", self.character_type)

        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)

    async def accept(self, interaction: discord.Interaction):
        self.state.item = self.random_item_set
        next_view = self.followup_view["view"](ctx=self.ctx, 
                                               data_loader=self.data_loader, 
                                               state=self.state, 
                                               character_type=self.character_type, 
                                               next_step=True)

        await interaction.response.edit_message(
            content=next_view.get_message(),
            view=next_view
        )
        

