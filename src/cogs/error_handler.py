from nextcord.ext import commands
from ..utils import errors
import nextcord
from wavelink.ext import spotify


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, errors.MemberNotInVoiceError):
            await interaction.send(
                content = '❌ **Join to voice a channel first**',
                ephemeral = True
            )
        elif isinstance(error, errors.BotNotInVoiceError):
            await interaction.send(
                content = '❌ **The bot is not in voice channel**',
                ephemeral = True
            )  
        elif isinstance(error, errors.BotIsNotPlayingError):
            await interaction.send(
                content = '❌ **The bot is not playing anything**',
                ephemeral = True
            )   
        elif isinstance(error, errors.BotIsAlreadyPausedError):
            await interaction.send(
                content = '❌ **The bot is already paused**',
                ephemeral = True
            )          
        elif isinstance(error, errors.BotIsAlreadyResumedError):
            await interaction.send(
                content = '❌ **The bot is already resumed**',
                ephemeral = True
            )  
        elif isinstance(error, errors.CommandIsNotInBoundChannelError):
            await interaction.send(
                content = '❌ **Commands are not support in this channel right now**',
                ephemeral = True
            )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))