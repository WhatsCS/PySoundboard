import threading
from datetime import timedelta
from pathlib import Path
from time import sleep

import simpleaudio as sa
from pydub import AudioSegment

#
# play_sound = signal('play-sound')
#
#
# @play_sound.connect
# def subscriber(sender, **kwargs):
#     AudioMaster(audio=kwargs.get('audio'))


class AudioMaster(threading.Thread):

    def __init__(self, audio):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = 'sound-Thread'
        self.length = None
        self.lengthStr = None
        self.play_audio = None
        self.audio = audio

        self.start()

    def run(self):
        self.audio_stream()

    def audio_stream(self):
        filepath = self.audio
        ext = filepath.rsplit('.')[1]

        # Get proper path (just assume it's shit)
        filepath = str(Path(filepath).resolve())

        # Get
        sound = AudioSegment.from_file(filepath, format=ext)
        self.length = int(sound.duration_seconds)
        self.lengthStr = str(
            timedelta(seconds=sound.duration_seconds)).rsplit('.')[0]

        self.play_audio = sa.play_buffer(sound.raw_data,
                                         num_channels=sound.channels,
                                         bytes_per_sample=sound.sample_width,
                                         sample_rate=sound.frame_rate)

        # # TODO: Remove/Alter as this is for testing
        while True:
            if not self.play_audio.is_playing():
                break
            sleep(1)


def stop_audio():
    sa.stop_all()
