from app.audio_processor import AudioProcessor
import numpy as np
import time

def test_audio():
    processor = AudioProcessor()
    processor.start_stream()
    
    print("Recording for 5 seconds...")
    
    try:
        for _ in range(50):  # ~5 seconds of readings
            data = processor.read_chunk()
            level = np.abs(data).mean()
            print(f"Signal level: {level:.6f}")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        processor.stream.stop_stream()
        processor.stream.close()
        processor.p.terminate()

if __name__ == "__main__":
    test_audio() 