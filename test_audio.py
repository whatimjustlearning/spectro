import numpy as np
import wave
import time
from app.audio_processor import AudioProcessor

def test_audio(filename="app/tmp/output.wav", duration=5):
    processor = AudioProcessor()
    print("\nAvailable audio devices:")
    for i in range(processor.p.get_device_count()):
        dev = processor.p.get_device_info_by_index(i)
        print(f"Device {i}: {dev['name']}")
    
    print(f"Using device index: {processor.device_index}")
    processor.start_stream()
    
    print(f"Recording for {duration} seconds...")
    
    frames = []
    
    try:
        for _ in range(int(processor.RATE / processor.CHUNK * duration)):
            data = processor.read_chunk()
            frames.append(data)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if processor.stream.is_active():
            processor.stream.stop_stream()
        processor.stream.close()
        processor.p.terminate()
    
    # Save the recorded frames as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(processor.CHANNELS)
        wf.setsampwidth(processor.p.get_sample_size(processor.FORMAT))
        wf.setframerate(processor.RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {filename}")

if __name__ == "__main__":
    test_audio()