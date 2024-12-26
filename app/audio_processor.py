import pyaudio
import numpy as np

class AudioProcessor:
    def __init__(self):
        self.CHUNK = 4096 * 2
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        
        # Find the IQAudio DAC device index
        self.device_index = self._find_device()
        
    def _find_device(self):
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            if "IQaudIO" in dev_info["name"]:
                return i
        raise RuntimeError("IQAudio DAC not found!")
    
    def start_stream(self):
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._callback
        )
        
    def _callback(self, in_data, frame_count, time_info, status):
        if status:
            print(f"Stream callback status: {status}")
        return (None, pyaudio.paContinue)
        
    def read_chunk(self):
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        return np.frombuffer(data, dtype=np.float32) 