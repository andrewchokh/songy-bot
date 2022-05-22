import nextcord
from nextcord.utils import get
from nextcord.ext import application_checks
from .errors import *


def member_in_voice():
    async def predicate(interaction: nextcord.Interaction):
        if not interaction.user.voice:
            raise MemberNotInVoiceError

        return True
    return application_checks.check(predicate) 


def bot_in_voice():
    async def predicate(interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        if not vc:
            raise BotNotInVoiceError

        return True
    return application_checks.check(predicate) 


def bot_is_playing():
    async def predicate(interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        if not vc.is_playing():
            raise BotIsNotPlayingError

        return True
    return application_checks.check(predicate) 


def bot_is_paused():
    async def predicate(interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        if vc.is_paused():
            raise BotIsAlreadyPausedError

        return True
    return application_checks.check(predicate) 


def bot_is_resumed():
    async def predicate(interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        if not vc.is_paused():
            raise BotIsAlreadyResumedError

        return True
    return application_checks.check(predicate)  


def cmd_in_bound_channel():
    async def predicate(interaction: nextcord.Interaction):
        vc = get(interaction.client.voice_clients, guild=interaction.guild)
        if vc.bound_channel is not interaction.channel:
            raise CommandIsNotInBoundChannelError

        return True
    return application_checks.check(predicate)  


# async def member_in_channel(ctx, send_reply=False):
#     check = ctx.author.voice

#     if not check and send_reply:
#         await ctx.reply('❌ **Join to voice channel first**')

#     return check 

# async def bot_in_channel(ctx, send_reply=False):
#     check = ctx.author.voice

#     if not check and send_reply:
#         await ctx.reply('❌ **Bot is not in voice channel**')    

#     return check

# async def bot_is_playing(ctx, send_reply=False):
#     check = ctx.voice_client.is_playing()

#     if not check and send_reply:
#         return await ctx.reply('❌ **Bot is not playing anything.**')   

#     return check    


# async def bot_is_paused(ctx, send_reply=False):
#     check = ctx.voice_client.is_paused()

#     if not check and send_reply:
#         await ctx.reply('❌ **Bot is already paused.**')  

#     return check 


# async def bot_is_resumed(ctx, send_reply=False):
#     check = ctx.voice_client.is_paused()

#     if not check and send_reply:
#         await ctx.reply('❌ **Bot is already resumed.**')      

#     return check 