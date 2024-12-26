import pyaudio
import numpy as np

class AudioProcessor:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("Initializing AudioProcessor class")
        self.CHUNK = 4096 * 2
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.logger.info("Creating PyAudio instance")
        self.p = pyaudio.PyAudio()
        
        # Find the IQAudio DAC device index
        self.logger.info("Listing available audio devices:")
        self.device_index = self._find_device()
        self.logger.info(f"Selected device index: {self.device_index}")
        
    def _find_device(self):
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            if "IQaudIO" in dev_info["name"]:
                return i
        raise RuntimeError("IQAudio DAC not found!")
    
    def start_stream(self):
        self.logger.info("Starting audio stream...")
        try:
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.CHUNK,
                stream_callback=self._callback
            )
            self.logger.info("Audio stream opened successfully")
        except Exception as e:
            self.logger.error(f"Failed to open audio stream: {e}", exc_info=True)
            raise
    
    def _callback(self, in_data, frame_count, time_info, status):
        if status:
            self.logger.warning(f"Stream callback status: {status}")
        return (None, pyaudio.paContinue)
        
    def read_chunk(self):
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.float32)
        except Exception as e:
            self.logger.error(f"Error reading chunk: {e}")
            raise