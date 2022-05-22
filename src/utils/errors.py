class MemberNotInVoiceError(Exception):
    def __init__(self, message: str = 'The member is not in a voice channel.'):            
        super().__init__(message)


class BotNotInVoiceError(Exception):
    def __init__(self, message: str = 'The bot is not in a voice channel.'):            
        super().__init__(message)


class BotIsNotPlayingError(Exception):
    def __init__(self, message: str = 'The bot is not playing anything.'):            
        super().__init__(message)


class BotIsAlreadyPausedError(Exception):
    def __init__(self, message: str = 'The bot is already paused.'):            
        super().__init__(message)


class BotIsAlreadyResumedError(Exception):
    def __init__(self, message: str = 'The bot is already resumed.'):            
        super().__init__(message)       


class CommandIsNotInBoundChannelError(Exception):
    def __init__(self, message: str = 'The command is not in a bound channel.'):            
        super().__init__(message)                    