from nextcord.ext import commands
import nextcord
import wavelink
from datetime import timedelta
from ..utils import logger
from ..utils import checks
from ..utils import track_embed
from wavelink.ext import spotify  
from nextcord.utils import get


GUILD_IDS = [831960677949505556, 837289438445830165]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # self.queue = {}
        # self.loop = {}
        # self.bound_channel = {}

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        logger.info(f'Started node <{node.identifier}>')     

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player, track, reason):
        # queue = self.queue[player.guild.id]

        # if self.loop[player.guild.id]:
        #     await player.play(track)
        # else:
        #     if queue.is_empty: return

        #     await player.play(queue.get())

        vc = get(self.bot.voice_clients, guild=player.guild)

        if vc.loop:
            return await vc.play(track)

        if not vc.queue.is_empty:
            await vc.play(vc.queue.get())

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     if after.channel is None:
    #         del self.queue[member.guild.id]
    #         del self.loop[member.guild.id]
    #         del self.bound_channel[member.guild.id]

    @nextcord.slash_command(
        name = 'join',
        description = 'Joins the bot to the voice channel',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    async def join(self, interaction: nextcord.Interaction):
        await interaction.user.voice.channel.connect(cls=wavelink.Player)

        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        setattr(vc, 'loop', False)
        setattr(vc, 'bound_channel', interaction.channel)

        await interaction.send(
            '🟢 **Joined `{0}` and bound to {1}**'.format(
                interaction.user.voice.channel.name, interaction.channel.mention
            )
        )

    @nextcord.slash_command(
        name = 'leave',
        description = 'Lol',
        guild_ids = GUILD_IDS
    )   
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.cmd_in_bound_channel()
    async def leave(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        await vc.disconnect()
        await interaction.send(f'🔴 **Leaved from `{interaction.user.voice.channel.name}`**') 

    @nextcord.slash_command(
        name = 'play',
        description = 'Plays the track from YouTube/Spotify',
        guild_ids = GUILD_IDS
    )  
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.cmd_in_bound_channel()
    async def play(
        self, 
        interaction: nextcord.Interaction,
        source: str = nextcord.SlashOption(
            name = 'source',
            description = 'A source of the track',
            choices = {
                'youtube': 'YOUTUBE',
                'spotify': 'SPOTIFY',
            },
            required = True
        ),
        track_search: str = nextcord.SlashOption(
            name = 'track',
            description = 'A track name or url',
            required = True
        )
    ):
        vc: wavelink.Player = get(
            interaction.client.voice_clients, guild=interaction.guild
        )

        if source == 'YOUTUBE':
            track = await wavelink.YouTubeTrack.search(query=track_search, return_first=True)
        elif source == 'SPOTIFY':
            try:
                track = await spotify.SpotifyTrack.search(query=track_search, return_first=True)
            except spotify.SpotifyRequestError:
                return await interaction.send(
                    content = '❌ **The track has not found. Use URL**',
                    ephemeral = True
                )

        vc.queue.put(track)

        if not vc.is_playing():
            await vc.play(vc.queue.get())
            
            emb = track_embed.make_embed(
                title = track.title,
                url = track.uri,
                color = 0xFF0000,
                thumbnail_url = track.info['thumbnail'],
                action = '🎵 Now playing',
                author = track.author,
                duration = timedelta(seconds=track.length),
                requester = str(interaction.user)
            )
        else:
            emb = track_embed.make_embed(
                title = track.title,
                url = track.uri,
                color = 0xFF0000,
                thumbnail_url = track.info['thumbnail'],
                action = '➕ Added to queue',
                author = track.author,
                duration = timedelta(seconds=track.length),
                requester = str(interaction.user),
                pos_queue = vc.queue.find_position(track) + 1
            )           

        await interaction.send(embeds=[emb]) 

    @nextcord.slash_command(
        name = 'stop',
        description = 'Stops the bot\'s playing',
        guild_ids = GUILD_IDS
    )   
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_playing()
    @checks.cmd_in_bound_channel()
    async def stop(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        await vc.stop()
        await interaction.send('⏹ **Stopped**')        

    @nextcord.slash_command(
        name = 'pause',
        description = 'Pauses on the current track',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_paused()
    @checks.cmd_in_bound_channel()
    async def pause(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        await vc.pause()
        await interaction.send('⏸ **Paused**') 

    @nextcord.slash_command(
        name = 'resume',
        description = 'Resumes on the current track',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_resumed()
    @checks.cmd_in_bound_channel()
    async def resume(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        await vc.resume()
        await interaction.send('▶ **Resumed**')

    @nextcord.slash_command(
        name = 'skip',
        description = 'Skips the current track',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_playing()
    @checks.cmd_in_bound_channel()
    async def skip(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        await vc.skip()
        await interaction.send('⏩ **Skipped**')    

    @nextcord.slash_command(
        name = 'loop',
        description = 'Loops the bot\'s playing',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.cmd_in_bound_channel()
    async def loop(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        try:
            vc.loop *= True
        except AttributeError:
            setattr(vc, 'loop', False)

        if vc.loop:
            await interaction.send('🔂 **Enabled**')
        else:
            await interaction.send('🔁 **Disabled**') 

    @nextcord.slash_command(
        name = 'current',
        description = 'Shows the current track',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_playing()
    @checks.cmd_in_bound_channel()
    async def current(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        track = vc.track
          
        emb = track_embed.make_embed(
            title = track.title,
            url = track.uri,
            color = 0xB500FF,
            thumbnail_url = track.info['thumbnail'],
            action = '🎶 Current track',
            author = track.author,
            duration = timedelta(seconds=track.length),
            requester = str(interaction.user)
        )

        await interaction.send(embeds=[emb])           

    @nextcord.slash_command(
        name = 'queue',
        description = 'Shows the queue',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.cmd_in_bound_channel()
    async def queue(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        emb = nextcord.Embed(title='Queue', color=0xFFFF00)

        if vc.queue.count:
            emb.description = ''
            for i, track in enumerate(vc.queue):
                emb.description += '{0}. [{1}]({2})\n'.format(
                    i + 1, track.info['title'], track.info['uri']
                )
            await interaction.send(embeds=[emb])      
        else:
            await interaction.send('📖 **Queue is empty**')      

    @nextcord.slash_command(
        name = 'clear-queue',
        description = 'Clears the queue'
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.cmd_in_bound_channel()
    async def clearqueue(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)

        vc.queue.clear()

        await interaction.send('📖 **Queue is cleared**')          

    @nextcord.slash_command(
        name = 'grab',
        description = 'Sends the current song to your direct',
        guild_ids = GUILD_IDS
    )
    @checks.member_in_voice()
    @checks.bot_in_voice()
    @checks.bot_is_playing()
    @checks.cmd_in_bound_channel()
    async def grab(self, interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        track = vc.track
          
        emb = track_embed.make_embed(
            title = track.title,
            url = track.uri,
            color = 0xB500FF,
            thumbnail_url = track.info['thumbnail'],
            action = '✉ Grabbed',
            author = track.author,
            duration = timedelta(seconds=track.length),
            requester = str(interaction.user)
        )

        await interaction.user.send(embeds=[emb])
        await interaction.send(f'✉ **Grabbed. Check your direct.**')             

    # @commands.command(name='connect', aliases=['join'])
    # async def connect(self, ctx: commands.Context):
    #     if not await checks.member_in_channel(ctx, True): return

    #     self.queue[ctx.guild.id] = wavelink.Queue(
    #         max_size=self.bot.cfg['queue_max_size']
    #     )
    #     self.loop[ctx.guild.id] = False
    #     self.bound_channel[ctx.guild.id] = ctx.channel

    #     await ctx.author.voice.channel.connect(cls=wavelink.Player)
    #     await ctx.reply(f'🟢 **Joined `{ctx.author.voice.channel.name}` and bound to {ctx.channel.mention}**')     

    # @commands.command(name='disconnect', aliases=['leave'])
    # async def disconnect(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
        
    #     await ctx.voice_client.disconnect()
    #     await ctx.reply(f'🔴 **Leaved from `{ctx.author.voice.channel.name}`**')          


    # @commands.command(name='play', aliases=['p'])
    # async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    #     if not ctx.voice_client:
    #         await self.connect(ctx)

    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return
    #     if not await checks.member_in_channel(ctx, True): return

    #     vc = ctx.voice_client
    #     queue = self.queue[ctx.guild.id]
    #     queue.put(search)  

    #     with ctx.typing():
    #         if not vc.is_playing():
    #             await vc.play(queue.get(), False)  
    #             await ctx.reply('🎵 **Playing `{0}` from YouTube**'.format(vc.source.info['title']))
    #         else:
    #             info = search.info

    #             emb = nextcord.Embed(
    #                 title=info['title'],
    #                 url=info['uri'],
    #                 color=0xFF0000
    #             )
    #             emb.set_thumbnail(url=info['thumbnail'])
    #             emb.set_author(
    #                 name='Added to queue',
    #                 icon_url=ctx.author.avatar.url
    #             )

    #             fields = [
    #                 {
    #                     'name': 'Channel', 
    #                     'value': info['author'], 
    #                     'inline': True
    #                 },
    #                 {
    #                     'name': 'Song Duration', 
    #                     'value': str(timedelta(seconds=search.length)), 
    #                     'inline': True
    #                 },
    #                 {
    #                     'name': 'Position in Queue', 
    #                     'value': queue.find_position(search) + 1, 
    #                     'inline': False
    #                 }
    #             ]

    #             for field in fields:
    #                 emb.add_field(
    #                     name=field['name'], 
    #                     value=field['value'], 
    #                     inline=field['inline']
    #                 )

    #             await ctx.reply(embeds=[emb])    

    # @commands.command()
    # async def splay(self, ctx: commands.Context, search: str):
    #     if not ctx.voice_client:
    #         await self.connect(ctx)

    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return
    #     if not await checks.member_in_channel(ctx, True): return

    #     vc = ctx.voice_client

    #     track = await spotify.SpotifyTrack.search(query=search, return_first=True)
    #     print(spotify.decode_url(search))

    #     queue = self.queue[ctx.guild.id]
    #     queue.put(track)

    #     if not vc.is_playing():
    #         await vc.play(queue.get())  
    #         await ctx.reply('🎵 **Playing `{0}` from YouTube**'.format(vc.source.info['title']))
    #     else:
    #         await ctx.reply('🎵 **Track `{0}` is put in query**'.format(vc.source.info['title']))

    # @commands.command(name='stop')
    # async def stop(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_playing(ctx, True): return   

    #     vc = ctx.voice_client
            
    #     self.loop[ctx.guild.id] = False
    #     await vc.stop() 
    #     await ctx.reply('⏹ **Stopped**') 

    # @commands.command(name='pause')
    # async def pause(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_paused(ctx, True): return   

    #     vc = ctx.voice_client
            
    #     await vc.pause()  
    #     await ctx.reply('⏸ **Paused**') 

    # @commands.command(name='resume')
    # async def resume(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_resumed(ctx, True): return   

    #     vc = ctx.voice_client
            
    #     await vc.resume()  
    #     await ctx.reply('⏸ **Resumed**')

    # @commands.command(name='skip')
    # async def skip(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_playing(ctx, True): return   

    #     vc = ctx.voice_client
    #     queue = self.queue[ctx.guild.id]
            
    #     await vc.play(queue.get())
    #     await ctx.reply('⏩ **Stopped**') 

    # @commands.command(name='loop')
    # async def loop(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return   

    #     if self.loop[ctx.guild.id]:
    #         self.loop[ctx.guild.id] = False
    #         msg = '🔁 **Disabled**'
    #     else:
    #         self.loop[ctx.guild.id] = True
    #         msg = '🔂 **Enabled**' 
            
    #     await ctx.reply(msg)                     

    # @commands.command(name='current')
    # async def current(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_playing(ctx, True): return

    #     vc = ctx.voice_client
    #     info = vc.source.info
          
    #     emb = nextcord.Embed(
    #         title=info['title'],
    #         url=info['uri'],
    #     )
    #     emb.set_thumbnail(url=info['thumbnail'])
    #     emb.set_author(
    #         name='Current Song',
    #         icon_url=ctx.author.avatar.url
    #     )

    #     fields = [
    #         {
    #             'name': 'Channel', 
    #             'value': info['author'], 
    #             'inline': True
    #         },
    #         {
    #             'name': 'Song Duration', 
    #             'value': str(timedelta(seconds=vc.source.length)), 
    #             'inline': True
    #         }
    #     ]

    #     for field in fields:
    #         emb.add_field(
    #             name=field['name'], 
    #             value=field['value'], 
    #             inline=field['inline']
    #         )

    #     await ctx.reply(embeds=[emb])       

    # @commands.command(name='queue')
    # async def queue(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
        
    #     queue = self.queue[ctx.guild.id]

    #     emb = nextcord.Embed(title='Queue', color=0xFFFF00)

    #     if queue.count:
    #         emb.description = ''
    #         for i, song in enumerate(queue):
    #             emb.description += '{0}. [{1}]({2})\n'.format(
    #                 i + 1, song.info['title'], song.info['uri']
    #             )
    #         await ctx.reply(embeds=[emb])      
    #     else:
    #         await ctx.reply('📖 **Queue is empty**')    

    # @commands.command(name='clearqueue')
    # async def clearqueue(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
        
    #     queue = self.queue[ctx.guild.id]

    #     if queue.count:
    #         queue.clear()

    #     await ctx.reply('🧹 **Queue cleared**') 

    # @commands.command(name='loop')
    # async def loop(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return   

    #     if self.loop[ctx.guild.id]:
    #         self.loop[ctx.guild.id] = False
    #         msg = '🔁 **Disabled**'
    #     else:
    #         self.loop[ctx.guild.id] = True
    #         msg = '🔂 **Enabled**' 
            
    #     await ctx.reply(msg)                     

    # @commands.command(name='grab')
    # async def grab(self, ctx: commands.Context):
    #     if ctx.channel != self.bound_channel[ctx.guild.id]: return

    #     if not await checks.member_in_channel(ctx, True): return
    #     if not await checks.bot_in_channel(ctx, True): return
    #     if not await checks.bot_is_playing(ctx, True): return

    #     vc = ctx.voice_client
    #     info = vc.source.info
          
    #     emb = nextcord.Embed(
    #         title=info['title'],
    #         url=info['uri'],
    #     )
    #     emb.set_thumbnail(url=info['thumbnail'])
    #     emb.set_author(
    #         name='Requested by {0}'.format(ctx.author),
    #         icon_url=ctx.author.avatar.url
    #     )

    #     fields = [
    #         {
    #             'name': 'Channel', 
    #             'value': info['author'], 
    #             'inline': True
    #         },
    #         {
    #             'name': 'Song Duration', 
    #             'value': str(timedelta(seconds=vc.source.length)), 
    #             'inline': True
    #         }
    #     ]

    #     for field in fields:
    #         emb.add_field(
    #             name=field['name'], 
    #             value=field['value'], 
    #             inline=field['inline']
    #         )

    #     await ctx.author.send(embeds=[emb])
    #     await ctx.reply(f'✉ **Grabbed. Check your direct.**')               


def setup(bot):
    bot.add_cog(Music(bot))