import discord

class FinalSetupView(discord.ui.View):
    def __init__(self, ctx, state):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.state = state

    def get_message(self):
        return (
            f'**{self.ctx.author.mention}**, your setup:'
            f'**Character:** {self.state.character}\n'
            f'**Perks:** {self.state.perks}\n'
        )