from pprint import pprint

import sounddevice as sd


def get_devs():
    pprint(sd.query_devices())


def get_curr():
    pass
