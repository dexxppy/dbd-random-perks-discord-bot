import discord

from core.data_loader import DataLoader
from core.state import SetupState
from views.character_randomize_view import CharacterRandomizeView


class StartSetupView(discord.ui.View):
    def __init__(self, ctx, character_type: str = None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.character_type = character_type

        btn_accept = discord.ui.Button(label=f"Let's go",
                                       style=discord.ButtonStyle.red,
                                       emoji="➡️")
        btn_accept.callback = self.accept
        self.add_item(btn_accept)

    def get_message(self):
        embeds = []

        embed = discord.Embed(
            title=f"🎲 DBD Random {self.character_type.capitalize()} Setup",
            description=f'*{self.ctx.author.mention}*, let\'s get You a randomized Setup for your next game!',
            color=discord.Color.dark_red()
        )

        embed.add_field(
            name="Setup contains of",
            value=("→ Character (survivor/killer) \n"
                   "→ Perks (all 4!) \n"
                   "→ Item and addons (survivor) \n"
                   "→ Addons (killer) \n"
                   "→ Offering \n"),
            inline=False
        )

        embed.add_field(
            name="Replacing objects",
            value="Anytime you get an object you do not have, replace it! Dropdowns are multiselect 😎\n"
        )

        embed.add_field(
            name="Rule #1 and only",
            value="Replace objects **only**, when you do not have it. Makes things funnier ❤️\n"
        )

        embed.set_thumbnail(url='https://yt3.googleusercontent.com/40AgRpxhy-LBqDUDyN4kyYX6iKVa3fVoO-ztUntBOrfxcsGdUFxMGgc2PJo98zxz7OtRfkLJeg=s900-c-k-c0x00ffffff-no-rj')
        embed.set_author(name="With ♥ by dexxppy", )
        embeds.append(embed)

        return {'content': None, 'embeds': embeds}

    async def accept(self, interaction: discord.Interaction):
        next_view = CharacterRandomizeView(
            ctx=self.ctx,
            data_loader=DataLoader(self.character_type),
            state=SetupState(self.ctx.author.id),
            character_type=self.character_type,
            next_step=True
        )

        msg = next_view.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=next_view
        )
