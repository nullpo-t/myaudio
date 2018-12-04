import sys
import pyaudio

pcm_bit = pyaudio.paInt16
pcm_rate = 48000
dev_input = 2  # `None`: use default device
buf_size = 1024

pa = pyaudio.PyAudio()
stream = pa.open(format=pcm_bit,
                 rate=pcm_rate,
                 channels=2,
                 frames_per_buffer=buf_size,
                 input=True,
                 input_device_index=dev_input,
                 output=False)
stream.start_stream()
while stream.is_active():
    buffer = stream.read(buf_size)
    if len(buffer) == 0:
        break
    sys.stdout.buffer.write(buffer)
stream.stop_stream()
stream.close()
pa.terminate()
