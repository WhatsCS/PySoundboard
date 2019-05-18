import blinker

from .audio import AudioMaster

play_sound = blinker.signal('play-sound')


# TODO: Build in a check for currently running audio so we don't overlap
@play_sound.connect
def subscriber(sender, **kwargs):
    AudioMaster(audio=kwargs.get('audio'))
