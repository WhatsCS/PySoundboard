'''
    PySoundboard is a pluggable (hopefully) and useful program to allow
    users to bind a key/GUI Button to any type of sound/video file.
'''
import argparse
import threading
import time

import yaml
from pynput import keyboard

from audio_lib.dispatch import play_song
from audio_lib.utils import get_devs, translate_keys

# ------ General Use Globals ------ #
# Create a playlist dictionary for easy processing
playlist: dict = {}


# ------ General Use Functions ------ #
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


# ------ Keyboard Monitoring and firing ------ #
do_quit = False
# currently active modifiers
current = set()


def on_press(key):
    global do_quit

    for k, v in playlist.items():
        if key in v[1]:
            current.add(key)
            if all(k in current for k in v[1]):
                play_song.send('anonymous', audio=playlist[k][0])

    if key == keyboard.Key.esc:
        do_quit = True


def on_release(key):
    global current
    try:
        current.remove(key)
    except:
        pass


# ------ Arg Parsing and Processing ------ #
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-r',
    '--run',
    action='store_true',
    help='will run program in bare-bones cli config polling for keypress')
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
        MainConfig = (yaml.safe_load(conf))
else:
    with open('config.yaml') as conf:
        MainConfig = (yaml.safe_load(conf))

# Fill the playlist
for key, value in MainConfig['Sound'].items():
    stuffs = {key: value}
    playlist.update(stuffs)
playlist = translate_keys(playlist)

# TODO: put in support for checking on currently running sound and create a queue or kill :shrug:
if args.song > 0:
    try:
        play_song.send('anonymous', audio=playlist[args.song][0])
        print("num of threads running: %s" % threading.active_count())
        t = threading.enumerate()
        print("threads:%r" % t)
        time.sleep(3)
        print("Double checkin shit bruv")
        time.sleep(7)
        print("closing shop")
    except KeyboardInterrupt:
        parser.exit(0, '\nInterrupted by user')
    except Exception as e:
        parser.exit(1, type(e).__name__ + ': ' + str(e))

if args.new_song is not None:
    # TODO: FIX THIS DOOD! IT BROKE AS HELL!
    with open('config.yaml', 'rw') as conf:
        # get last sound so we can increment
        l_sound = MainConfig['Sound'].popitem()
        n_sound = {l_sound[0] + 1: {'': args.new_song}}
        yaml.dump(n_sound, conf)

if args.run:
    try:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
        ).start()
        while True:
            if do_quit:
                break
            time.sleep(0.05)
    except KeyboardInterrupt:
        parser.exit(0, '\nInterrupted by user')
