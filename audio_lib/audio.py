import threading
from datetime import timedelta
from pathlib import Path
from time import sleep

import simpleaudio as sa
from pydub import AudioSegment

#
# play_song = signal('play-song')
#
#
# @play_song.connect
# def subscriber(sender, **kwargs):
#     AudioMaster(audio=kwargs.get('audio'))


class AudioMaster(threading.Thread):

    def __init__(self, audio):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = 'Song-Thread'
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
        song = AudioSegment.from_file(filepath, format=ext)
        self.length = int(song.duration_seconds)
        self.lengthStr = str(
            timedelta(seconds=song.duration_seconds)).rsplit('.')[0]

        self.play_audio = sa.play_buffer(song.raw_data,
                                         num_channels=song.channels,
                                         bytes_per_sample=song.sample_width,
                                         sample_rate=song.frame_rate)

        # TODO: Remove/Alter as this is for testing
        x = 0
        while x is not 10:
            print(str(timedelta(seconds=self.length)).rsplit('.')[0])
            if not self.play_audio.is_playing():
                break
            sleep(1)
            self.length -= 1
            x += 1
        stop_audio()


def stop_audio():
    sa.stop_all()
