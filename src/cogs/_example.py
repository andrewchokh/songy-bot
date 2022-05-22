from nextcord.ext import commands
import nextcord


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Some incrediable code


def setup(bot):
    bot.add_cog(Example(bot))