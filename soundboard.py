'''
    PySoundboard is a pluggable (hopefully) and useful program to allow
    users to bind a key/GUI Button to any type of sound/video file.
'''
import argparse
import os
import queue
from typing import Any, Tuple

import sounddevice as sd
import threading
import yaml
import blinker
from audio_lib.audio import AudioMaster, stop_audio
from audio_lib.utils import get_devs
import audio_lib.dispatch
from pprint import pprint
import time
from collections import OrderedDict


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c',
                    '--config',
                    default=None,
                    help='load config from non-standard location')
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
parser.add_argument('-s', '--song', type=int, default=0, help='play song #')
parser.add_argument('-ld',
                    '--list-devices',
                    action='store_true',
                    help='get list of available devices')
parser.add_argument('-ns',
                    '--new-song',
                    type=str,
                    default=None,
                    help='adds a new song to the config')
# TODO: Add in --gui argument
args = parser.parse_args()
if args.blocksize == 0:
    parser.error('blocksize must not be zero')
if args.buffersize < 1:
    parser.error('buffersize must be at least 1')
if args.list_devices is True:
    get_devs()

# Load config into args (for now)
if args.config is not None:
    with open(args.config) as conf:
        MainConfig = OrderedDict(yaml.safe_load(conf))
else:
    with open('config.yaml') as conf:
        MainConfig = OrderedDict(yaml.safe_load(conf))

playlist: dict = {}
i = 1
for key, value in MainConfig.items():
    if key == i:
        for k, v in value.items():
            if k == 'filename':
                songs = {i: v}
                playlist.update(songs)
    i += 1
play_song = blinker.signal('play-song')

if args.song > 0:
    try:
        play_song.send('anonymous', audio=playlist[args.song])
        print("num of threads running: %s" % threading.active_count())
        t = threading.enumerate()
        print("threads:%r" % t)
        time.sleep(3)
        print("Double checkin shit bruv")
        time.sleep(7)
        print("closing shop")
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

if args.new_song is not None:
    with open('config.yaml', 'a') as conf:
        # get last sound so we can increment
        l_sound = MainConfig.popitem()
        n_sound = {l_sound[0] + 1: {'filename': args.new_song}}
        yaml.dump(n_sound, conf)
