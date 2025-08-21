import discord

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
        character = self.state.character["survivor_name"]
        perks = [{"perk_name": perk["perk_data"]["survivor_perk_name"]} for perk in self.state.perks]
        item = {
            "item": self.state.item["item"]["survivor_item_name"],
            "addons": [
                addon["addon_data"]["survivor_addon_name"]
                for addon in self.state.item["addons"]
            ]
        }
        offering = self.state.offering["offering_name"]

        embed = discord.Embed(
            title="🎲 Your Randomized Setup",
            description=f"{self.ctx.author.mention}, this is your summary:",
            color=discord.Color.red()
        )

        embed.add_field(
            name="→ Your survivor:",
            value=f"*{character}*",
            inline=False
        )

        perks_value = []
        for perk in perks:
            perks_value.append(f'*{perk["perk_name"]}*')

        embed.add_field(
            name="→ Your perks:",
            value="\n".join(perks_value),
            inline=False
        )

        item_value = [f'*{item["item"]}*']

        for addon in item["addons"]:
            item_value.append(f'+ *{addon}*')

        embed.add_field(
            name="→ Your Item Set:",
            value="\n".join(item_value),
            inline=False
        )

        embed.add_field(
            name="→ Your offering:",
            value=f"*{offering}*",
            inline=False
        )

        embed.set_thumbnail(url='https://yt3.googleusercontent.com/40AgRpxhy-LBqDUDyN4kyYX6iKVa3fVoO-ztUntBOrfxcsGdUFxMGgc2PJo98zxz7OtRfkLJeg=s900-c-k-c0x00ffffff-no-rj')
        embed.set_footer(text="Good luck, have fun!")
        return embed
        
    def get_killer_message(self):
        character = self.state.character["killer_name"]
        perks = [{"perk_name": perk["perk_data"]["killer_perk_name"]} for perk in self.state.perks]
        addons = [{"addon_name": addon["addon_data"]["killer_addon_name"]} for addon in self.state.killer_addons]
        offering = self.state.offering["offering_name"]

        embed = discord.Embed(
            title="🎲 Your Randomized Setup",
            description=f"{self.ctx.author.mention}, this is your summary:",
            color=discord.Color.red()
        )

        embed.add_field(
            name="→ Your killer:",
            value=f"*{character}*",
            inline=False
        )

        perks_value = []
        for perk in perks:
            perks_value.append(f'*{perk["perk_name"]}*')

        embed.add_field(
            name="→ Your perks:",
            value="\n".join(perks_value),
            inline=False
        )

        addons_value = []
        for addon in addons:
            addons_value.append(f'+ *{addon["addon_name"]}*')

        embed.add_field(
            name="→ Your Addon Set:",
            value="\n".join(addons_value),
            inline=False
        )

        embed.add_field(
            name="→ Your offering:",
            value=f"*{offering}*",
            inline=False
        )

        embed.set_thumbnail(url='https://yt3.googleusercontent.com/40AgRpxhy-LBqDUDyN4kyYX6iKVa3fVoO-ztUntBOrfxcsGdUFxMGgc2PJo98zxz7OtRfkLJeg=s900-c-k-c0x00ffffff-no-rj')
        embed.set_footer(text="Good luck, have fun!")

        return embed
        
    def get_message(self):
        return self.message_function()