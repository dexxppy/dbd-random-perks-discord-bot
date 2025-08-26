import discord

from core.data_loader import DataLoader
from core.state import SetupState
from utils.views_utils import get_options_for_select
from views.final_setup_view import FinalSetupView


class BaseRandomizeView(discord.ui.View):
    def __init__(self, ctx, data_loader: DataLoader, state: SetupState, character_type: str = None,
                 next_step: bool = True, followup_view=None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.data_loader = data_loader
        self.state = state
        self.character_type = character_type
        self.next_step = next_step
        self.select = None
        self.selected_ids = []
        self.followup_view = followup_view.get(self.character_type)

    def get_message(self) -> str:
        raise NotImplementedError

    def get_accept_button(self):
        if self.next_step and self.followup_view:
            btn_accept = discord.ui.Button(label=f"Continue with {self.followup_view['next_drawn']}",
                                           style=discord.ButtonStyle.success, emoji="➡️")
            btn_accept.callback = self.accept
            self.add_item(btn_accept)

    def get_replace_button(self, replace_value: str, replace_func=None):
        if replace_func is None:
            replace_func = self.replace

        replace_btn = discord.ui.Button(label=f"Replace {replace_value}", style=discord.ButtonStyle.primary, emoji="🔃")
        replace_btn.callback = replace_func
        self.add_item(replace_btn)

    def get_select(self, options, object_type, min_values, max_values):
        self.select = discord.ui.Select(
            placeholder=f"Choose {object_type}s to replace",
            min_values=min_values,
            max_values=max_values,
            options=get_options_for_select(options, object_type, self.character_type)
        )

        self.select.callback = self.handle_select
        self.add_item(self.select)

    def randomize(self):
        raise NotImplementedError

    async def accept(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def replace(self, interaction: discord.Interaction):
        self.randomize()

        msg = self.get_message()
        content = msg['content']
        embeds = msg['embeds']

        await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            view=self
        )

    async def handle_select(self, interaction: discord.Interaction):
        self.selected_ids = [int(value) for value in self.select.values]
        await interaction.response.defer()
