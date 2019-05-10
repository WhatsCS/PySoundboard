# PySoundboard
a fuckin soundboard, I think

```
usage: soundboard.py [-h] [-c CONFIG] [-d DEVICE] [-b BLOCKSIZE]
                     [-q BUFFERSIZE] [-s SONG] [-ld] [-ns NEW_SONG]

PySoundboard is a pluggable (hopefully) and useful program to allow users to
bind a key/GUI Button to any type of sound/video file.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        load config from non-standard location
  -d DEVICE, --device DEVICE
                        output device (numeric ID or substring)
  -b BLOCKSIZE, --blocksize BLOCKSIZE
                        block size (default: 2048)
  -q BUFFERSIZE, --buffersize BUFFERSIZE
                        number of blocks used for buffering (default: 20)
  -s SONG, --song SONG  play song #
  -ld, --list-devices   get list of available devices
  -ns NEW_SONG, --new-song NEW_SONG
                        adds a new song to the config
```
