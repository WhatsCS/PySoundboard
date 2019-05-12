import blinker

from .audio import AudioMaster

play_song = blinker.signal('play-song')


# TODO: Build in a check for currently running audio so we don't overlap
@play_song.connect
def subscriber(sender, **kwargs):
    AudioMaster(audio=kwargs.get('audio'))
