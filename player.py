import sys
import pyaudio

pcm_bit = pyaudio.paInt16
pcm_rate = 48000
dev_output = 2  # `None`: use default device
buf_size = 1024

while True:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pcm_bit,
                     rate=pcm_rate,
                     channels=2,
                     frames_per_buffer=buf_size,
                     input=False,
                     output=True,
                     output_device_index=dev_output)
    stream.start_stream()
    try:
        while stream.is_active():
            try:
                buffer = sys.stdin.buffer.read(buf_size)
            except OSError:
                buffer = b'\x00' * buf_size
            if len(buffer) == 0:
                break
            stream.write(buffer)
        stream.stop_stream()
        stream.close()
        pa.terminate()
    except OSError:
        pass
