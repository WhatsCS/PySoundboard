from pprint import pprint
import pysnooper
import string
import sounddevice as sd
from pynput.keyboard import Key, KeyCode

key_map = {
    'ctrl': Key.ctrl_l,
    'lctrl': Key.ctrl_l,
    'rctrl': Key.ctrl_r,
    'shift': Key.shift,
    'alt': Key.alt
}


def get_devs():
    pprint(sd.query_devices())


def get_curr():
    pass


# @pysnooper.snoop()
def translate_keys(tl_arg):
    if type(tl_arg) is dict:
        for i in range(1, len(tl_arg) + 1):
            keys = tl_arg[i][1].split('+')
            for item in keys:
                if item in list(string.ascii_letters) or item in list(string.digits):
                    keys[keys.index(item)] = KeyCode(char=item)
                else:
                    keys[keys.index(item)] = key_map[item]
            tl_arg[i][1] = set(keys)
    # if type(tl_arg) is list:

    return tl_arg
