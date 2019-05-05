from pydub import AudioSegment
from datetime import timedelta
from time import sleep
import pysnooper
import simpleaudio as sa
import sys


@pysnooper.snoop()
def play_file(args):
    ''' 
    Takes a file path and play the destination file for full length of time.
    '''

    file = args['filename']
    ext = file.rsplit('.')[1]

    song = AudioSegment.from_file(file, format=ext)
    length = str(timedelta(seconds=song.duration_seconds)).rsplit('.')[0]

    play_audio = sa.play_buffer(song.raw_data,
                                num_channels=song.channels,
                                bytes_per_sample=song.sample_width,
                                sample_rate=song.frame_rate)

    while True:
        if not play_audio.is_playing():
            break
        sleep(10)
        stop_audio()


def stop_audio():
    sa.stop_all()