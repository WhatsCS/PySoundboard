import blinker
from .audio import AudioMaster

play_song = blinker.signal('play-song')


@play_song.connect
def subscriber(sender, **kwargs):
    AudioMaster(audio=kwargs.get('audio'))
