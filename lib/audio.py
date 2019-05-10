from pydub import AudioSegment
from datetime import timedelta
from time import sleep
from pathlib import Path
from blinker import signal
import pysnooper
import simpleaudio as sa
import sys
import threading

play_song = signal('play-song')


@play_song.connect
def subscriber(sender, **kwargs):
    am = kwargs.get('am')
    am.audio_stream(kwargs.get('audio'))
    print("playing music")
    am.start()


class AudioMaster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.length = None
        self.lengthStr = None
        self.play_audio = None

    def run(self):
        self.play()

    def audio_stream(self, audio: str):
        filepath = audio
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

    def play(self):
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