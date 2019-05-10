'''
    PySoundboard is a pluggable (hopefully) and useful program to allow
    users to bind a key/GUI Button to any type of sound/video file.
'''
import argparse
import os
import queue
import sounddevice as sd
import threading
import yaml
import blinker
from lib.audio import AudioMaster, stop_audio
from lib.utils import get_devs
from pprint import pprint


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c',
                    '--config',
                    help='load config from non-standard location',
                    default='None')
parser.add_argument('-d',
                    '--device',
                    type=int_or_str,
                    help='output device (numeric ID or substring)')
parser.add_argument('-b',
                    '--blocksize',
                    type=int,
                    default=2048,
                    help='block size (default: %(default)s)')
parser.add_argument(
    '-q',
    '--buffersize',
    type=int,
    default=20,
    help='number of blocks used for buffering (default: %(default)s)')
parser.add_argument('-ld',
                    '--list-devices',
                    action='store_true',
                    help='get list of available devices')
# parser.add_argument('--stop-playback',
#                     action='store_true',
#                     default=False,
#                     help='Stops all audio playback')
# TODO: Add in --gui argument
args = parser.parse_args()
if args.blocksize == 0:
    parser.error('blocksize must not be zero')
if args.buffersize < 1:
    parser.error('buffersize must be at least 1')
if args.list_devices is True:
    get_devs()
# if args.stop_playback is True:
#     stop_audio()
#     parser.exit(0, 'Audio Stopped!')

# Load config into args (for now)
with open('config.yaml') as conf:
    MainConfig = yaml.safe_load(conf)

#TODO: this will not stay static...
config = dict(MainConfig['SoundConfig'])
config.update(vars(args))

playlist: dict = {}
i = 1
for key, value in config.items():
    if key == 'Sound-' + str(i):
        for k, v in value.items():
            if k == 'filename':
                songs = {i: v}
                playlist.update(songs)
    i += 1
play_song = blinker.signal('play-song')
am = AudioMaster()

soin = 1

try:
    if soin == 1:
        play_song.send('anonymous', am=am, audio=playlist[soin])
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
