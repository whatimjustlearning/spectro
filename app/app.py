from flask import Flask, render_template, send_file
import os
import wave
import threading
import time
from audio_processor import AudioProcessor
import numpy as np
import matplotlib.pyplot as plt

import os
print("Current working directory:", os.getcwd())

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def record_and_process():
    processor = AudioProcessor()
    processor.start_stream()
    
    while True:
        frames = []
        for _ in range(int(processor.RATE / processor.CHUNK * 2)):  # 2 seconds
            data = processor.read_chunk()
            frames.append(data)
        
        # Save the recorded frames as a WAV file
        filename = os.path.join(UPLOAD_FOLDER, 'current.wav')
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(processor.CHANNELS)
            wf.setsampwidth(processor.p.get_sample_size(processor.FORMAT))
            wf.setframerate(processor.RATE)
            wf.writeframes(b''.join(frames))
        
        # Generate spectrogram
        generate_spectrogram(filename)
        
        time.sleep(0.1)  # Short delay to prevent CPU overload

def generate_spectrogram(wav_file):
    sample_rate, data = wave.open(wav_file)
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    
    plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='viridis')
    plt.axis('off')
    plt.savefig(os.path.join(UPLOAD_FOLDER, 'spectrogram.png'), bbox_inches='tight', pad_inches=0)
    plt.close()

@app.route('/')
def index():
    return render_template('/home/spectro/templates/index.html')

@app.route('/spectrogram')
def get_spectrogram():
    return send_file(os.path.join(UPLOAD_FOLDER, 'spectrogram.png'), mimetype='image/png')

if __name__ == "__main__":
    threading.Thread(target=record_and_process, daemon=True).start()
    app.run(debug=True)