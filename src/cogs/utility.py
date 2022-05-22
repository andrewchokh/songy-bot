from turtle import width
from nextcord.ext import commands
import nextcord


GUILD_IDS = [831960677949505556, 837289438445830165]


class EmbedModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            'Embed Maker'
        )

        self.embTitle = nextcord.ui.TextInput(
            label = 'Title', max_length = 256, placeholder = 'Title', row = 1,
        )
        self.add_item(self.embTitle)

        self.embTitleURL = nextcord.ui.TextInput(
            label = 'Title URL', placeholder = 'Title URL', row = 1
        )
        self.add_item(self.embTitleURL)

        self.embDesc = nextcord.ui.TextInput(
            label = 'Description', 
            max_length = 2048, 
            placeholder = 'Description', 
            row = 3, 
            style = nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.embDesc)

    async def callback(self, interaction: nextcord.Interaction):
           title = self.embTitle.value
           desc = self.embDesc.value
           title_url = self.embTitleURL.value
           emb = nextcord.Embed(title=title, description=desc, url = title_url)
           return await interaction.response.send_message(embed=emb)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name = 'embed',
        description = 'Makes a custom embed',
        guild_ids = GUILD_IDS
    )
    async def embed(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EmbedModal())

def setup(bot):
    bot.add_cog(Utility(bot))