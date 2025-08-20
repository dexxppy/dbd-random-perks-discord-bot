import discord

from core.data_loader import DataLoader
from core.state import SetupState


class FinalSetupView(discord.ui.View):
    def __init__(self, ctx, state: SetupState, character_type: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.state = state
        self.message_function = {
            "survivor": self.get_survivor_message,
            "killer": self.get_killer_message
        }.get(character_type)

    def get_survivor_message(self):
        return "nice"
        # character = self.state.character["survivor_name"]
        # perks = [{"perk_name": perk["perk_data"]["survivor_perk_name"], "perk_owner": perk["perk_data"]["survivor_owner_name"]} for perk in self.state.perks]
        # item = {
        #     "item": {
        #         "item_name": self.state.item["item"]["survivor_item_name"],
        #         "item_rarity": self.state.item["item"]["survivor_item_rarity"]},
        #     "addons": [
        #         {
        #             "addon_name": addon["addon_data"]["survivor_addon_name"],
        #             "addon_rarity": addon["addon_data"]["survivor_addon_rarity"],
        #         }
        #         for addon in self.state.item["addons"]
        #     ]
        # }
        # offering = {
        #     "offering_name": self.state.offering["offering_name"],
        #     "offering_rarity":self.state.offering["offering_rarity"]
        # }
        #
        # msg_character = " ".join([
        #     "**Your Survivor**:",
        #     f'{character}'
        # ])
        #
        # msg_perks = "\n".join([
        #     "**Your Perks**:",
        #     *[f'→ **{perk["perk_name"]}** from *{perk["perk_owner"]}*'
        #     for perk in perks]
        # ])
        #
        # msg_item = "\n".join([
        #     "**Your Item Set**:",
        #     f'→ **{item["item"]["item_name"]}** of *{item["item"]["item_rarity"]}* rarity',
        #     *[f'→ **{addon["addon_name"]}** of *{addon["addon_rarity"]}* rarity'
        #     for addon in item["addons"]]
        # ])
        #
        # msg_offering = "\n".join([
        #     "**Your Offering**:",
        #     f'**{offering["offering_name"]}** of *{offering["offering_rarity"]}* rarity'
        # ])
        #
        #
        # return (
        #     f'**{self.ctx.author.mention}**, this is your final setup: \n'
        #     f'{msg_character}\n'
        #     f'{msg_perks}\n'
        #     f'{msg_item}\n'
        #     f'{msg_offering}\n'
        # )
        
    def get_killer_message(self):
        character = self.state.character["killer_name"]
        perks = [{"perk_name": perk["perk_data"]["killer_perk_name"], "perk_owner": perk["perk_data"]["killer_owner_name"]} for perk in self.state.perks]
        addons = [
            {
                "addon_name": addon["addon_data"]["killer_addon_name"],
                "addon_rarity": addon["addon_data"]["killer_addon_rarity"],
            }
            for addon in self.state.killer_addons
        ]

        offering = {
            "offering_name": self.state.offering["offering_name"],
            "offering_rarity":self.state.offering["offering_rarity"]
        }
        
        
        return (
            f'**{self.ctx.author.mention}**, your setup:'
            f'**Character:** {character}\n'
            f'**Perks:** {perks}\n'
            f'**Item:** {addons}\n'
            f'**Offering:** {offering}\n'
        )
        
    def get_message(self):
        print(self.message_function())
        return self.message_function()