import json
from dotenv import load_dotenv
import nextcord
from src.bot import Bot
import os  
import wavelink
from wavelink.ext import spotify


def load_json(filename):
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)


async def node_connect(bot, opts):
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=bot,
        host=opts['host'],
        port=opts['port'],
        password=opts['password'],
        https=opts['https'],
        spotify_client=spotify.SpotifyClient(
            client_id=opts['spotify_client_id'],
            client_secret=os.getenv('SPOTIFY_SECRET_ID')
        )
    )


def main():
    load_dotenv()

    bot = Bot(
        intents=nextcord.Intents.all(),
        cfg=load_json('./src/cfgs/bot.json')
    )

    node_opts = load_json('./src/cfgs/node.json')

    bot.loop.create_task(node_connect(bot, node_opts))

    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()