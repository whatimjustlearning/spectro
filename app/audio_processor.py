import pyaudio
import numpy as np
import time

class AudioProcessor:
    def __init__(self):
        time.sleep(30)
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
            frames_per_buffer=self.CHUNK
        )
        
    def read_chunk(self):
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.float32)
        except Exception as e:
            self.logger.warning(f"Warning reading chunk: {e}")
            # Return silence instead of raising an error
            return np.zeros(self.CHUNK, dtype=np.float32)