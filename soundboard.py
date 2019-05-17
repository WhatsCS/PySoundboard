'''
    PySoundboard is a pluggable (hopefully) and useful program to allow
    users to bind a key/GUI Button to any type of sound/video file.
'''
import argparse
import threading
import time

import yaml
from pynput import keyboard

from audio_lib.audio import stop_audio
from audio_lib.dispatch import play_sound
from audio_lib.utils import get_devs, translate_keys

# ------ General Use Globals ------ #
# Create a playlist dictionary for easy processing
playlist: dict = {}
gen_keybinds = {}


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

    for k, val in playlist.items():
        if key in val:
            current.add(key)
            if all(k in current for k in val):
                play_sound.send('anonymous', audio=playlist[k][0])
    for k, val in gen_keybinds.items():
        if key in val:
            current.add(key)
            if all(k in current for k in val):
                if k == 'quit':
                    do_quit = True
                if k == 'stop':
                    stop_audio()

    # if key == keyboard.Key.esc:
    #     do_quit = True


def on_release(key):
    global current
    try:
        current.remove(key)
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))
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
parser.add_argument('-s', '--sound', type=int, default=0, help='play sound #')
parser.add_argument('-ld',
                    '--list-devices',
                    action='store_true',
                    help='get list of available devices')
parser.add_argument('-ns',
                    '--new-sound',
                    type=str,
                    default=None,
                    nargs='+',
                    help='adds a new sound to the config')
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
    v = [value[0], translate_keys(value[1])]
    stuffs = {key: v}
    playlist.update(stuffs)

# Fill general use keybinds
for key, value in MainConfig['General']['keybinds'].items():
    v = translate_keys(value)
    stuffs = {key: v}
    gen_keybinds.update(stuffs)

# TODO: put in support for checking on currently running sound and create a queue or kill :shrug:
if args.sound > 0:
    try:
        play_sound.send('anonymous', audio=playlist[args.sound][0])
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

if args.new_sound is not None:
    if len(args.new_sound) is 1:
        with open('config.yaml', 'a') as conf:
            n_sound = {len(MainConfig['Sound']) + 1: [args.new_sound[0], '']}
            yaml.dump(n_sound, conf)
    else:
        with open('config.yaml', 'w') as conf:
            config = MainConfig
            n_sound = {
                len(MainConfig['Sound']) + 1:
                [args.new_sound[0], args.new_sound[1].strip('\'')]
            }
            config['Sound'].update(n_sound)
            yaml.dump(config, conf)

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
