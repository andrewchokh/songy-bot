from nextcord.ext import commands
from src.utils import logger
import os


class Bot(commands.Bot):
    def __init__(self, intents, cfg):
        super().__init__(
            command_prefix=cfg['prefix'],
            intents=intents
        )
        self.cfg = cfg

        self.load_cogs('./src/cogs')   

    def load_cogs(self, path):
        for file in os.listdir(path):
            if not file.startswith('_') and file.endswith('.py'):
                self.load_extension(f'src.cogs.{file[:-3]}')
                logger.info(f'Loaded cog "{ file[:-3]}"')     

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Logged as {str(self.user)}')                      


    def run(self, token):
        super().run(token)