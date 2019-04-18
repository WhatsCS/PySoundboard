"""
async def play_buffer(buffer, **kwargs):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    idx = 0

    def callback(outdata, frame_count, time_info, status):
        nonlocal idx
        if status:
            print(status)
        remainder = len(buffer) - idx
        if remainder == 0:
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop
        valid_frames = frame_count if remainder >= frame_count else remainder
        outdata[:valid_frames] = buffer[idx:idx + valid_frames]
        outdata[valid_frames:] = 0
        idx += valid_frames

    stream = sd.OutputStream(callback=callback, dtype=buffer.dtype,
                             channels=buffer.shape[1], **kwargs)
    with stream:
        await event.wait()
"""
import sounddevice as sd
import soundfile as sf
import sys
from pprint import pprint


class Audio:
    def __init__(self, args, queue, event, fobj):
        self.args = args
        self.queue = queue
        self.event = event
        self.fobj = fobj

    def _callback(self, outdata, frames, time, status):
        assert frames == self.args['blocksize']
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = self.queue.get_nowait()
        except self.queue.Empty:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data

    def play_file(self):
        with sf.SoundFile(self.args["filename"]) as f:
            for _ in range(self.args["buffersize"]):
                data = f.buffer_read(self.args["blocksize"], dtype='float32')
                if not data:
                    break
                self.queue.put_nowait(data)  # Pre-fill queue

            stream = sd.RawOutputStream(
                samplerate=f.samplerate,
                blocksize=self.args["blocksize"],
                device=self.args["device"],
                channels=f.channels,
                dtype='float32',
                callback=self._callback,
                finished_callback=self.event.set)
            with stream:
                timeout = self.args["blocksize"] * self.args[
                    "buffersize"] / f.samplerate
                while data:
                    data = f.buffer_read(
                        self.args["blocksize"], dtype='float32')
                    self.queue.put(data, timeout=timeout)
                self.event.wait()  # Wait until playback is finished