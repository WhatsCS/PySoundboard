'''
    PySoundboard is a pluggable (hopefully) and useful program to allow
    users to bind a key/GUI Button to any type of sound/video file.
'''
import argparse
import queue
import sounddevice as sd
import threading
from lib.audio import Audio
from lib.utils import get_devs


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('filename', help='audio file to be played back')
parser.add_argument(
    '-d',
    '--device',
    type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-b',
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
parser.add_argument(
    '-ld',
    '--list-devices',
    action='store_true',
    help='get list of available devices')
# TODO: Add in --gui argument
args = parser.parse_args()
if args.blocksize == 0:
    parser.error('blocksize must not be zero')
if args.buffersize < 1:
    parser.error('buffersize must be at least 1')
if args.list_devices is True:
    get_devs()

# Create thread pool
q = queue.Queue(maxsize=args.buffersize)
event = threading.Event()

try:
    Audio(args, q, event).play_file()
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except queue.Full:
    # A timeout occured, i.e. there was an error in the callback
    parser.exit(1)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
