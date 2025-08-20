import discord

from core.data_loader import DataLoader
from core.state import SetupState
from views.final_setup_view import FinalSetupView


class BaseRandomizeView(discord.ui.View):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type: str = None, next_step: bool = True, followup_view = None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.data_loader = data_loader
        self.state = state
        self.character_type = character_type
        self.next_step = next_step
        self.select = None
        self.selected_ids = []
        self.followup_view = followup_view.get(self.character_type)

        if self.next_step and self.followup_view:
            btn_accept = discord.ui.Button(label=f"Continue with {self.followup_view['next_drawn']} ➡", style=discord.ButtonStyle.success)
            btn_accept.callback = self.accept
            self.add_item(btn_accept)

    def get_message(self) -> str:
        raise NotImplementedError

    def randomize(self):
        raise NotImplementedError

    async def accept(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def replace(self, interaction: discord.Interaction):
        self.randomize()
        content = self.get_message()
        await interaction.response.edit_message(content=content, view=self)

    async def handle_select(self, interaction: discord.Interaction):
        self.selected_ids = [int(value) for value in self.select.values]
        await interaction.response.defer()


