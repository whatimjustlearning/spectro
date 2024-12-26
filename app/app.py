from flask import Flask, render_template, send_file
import os
import wave
import threading
import time
from audio_processor import AudioProcessor
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
print("Current working directory:", os.getcwd())

app = Flask(__name__, template_folder='/home/spectro/app/templates')
UPLOAD_FOLDER = 'uploads'
TMP_FOLDER = 'tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TMP_FOLDER, exist_ok=True)

def record_and_process():
    processor = AudioProcessor()
    processor.start_stream()
    
    logging.info("Audio stream started")
    
    while True:
        frames = []
        for _ in range(int(processor.RATE / processor.CHUNK * 2)):  # 2 seconds
            logging.info("Reading chunk")
            data = processor.read_chunk()
            frames.append(data)
        
        # Save the recorded frames as a WAV file
        filename = os.path.join(TMP_FOLDER, 'current.wav')
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(processor.CHANNELS)
            wf.setsampwidth(processor.p.get_sample_size(processor.FORMAT))
            wf.setframerate(processor.RATE)
            wf.writeframes(b''.join(frames))
            
        logging.info("Saved WAV file")
        
        # Generate spectrogram
        generate_spectrogram(filename)
        
        logging.info("Generated spectrogram")
        
        time.sleep(0.1)  # Short delay to prevent CPU overload

def generate_spectrogram(wav_file):
    sample_rate, data = scipy.io.wavfile.read(wav_file)
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    
    plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='viridis')
    plt.axis('off')
    plt.savefig(os.path.join(UPLOAD_FOLDER, 'spectrogram.png'), bbox_inches='tight', pad_inches=0)
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spectrogram')
def spectrogram_page():
    return render_template('spectrogram.html')

@app.route('/spectrogram-image')
def get_spectrogram():
    spectrogram_path = os.path.join(UPLOAD_FOLDER, 'spectrogram.png')
    
    if not os.path.exists(spectrogram_path):
        # Generate an empty spectrogram
        plt.figure(figsize=(10, 4))
        plt.text(0.5, 0.5, 'Waiting for audio...', 
                horizontalalignment='center',
                verticalalignment='center')
        plt.axis('off')
        plt.savefig(spectrogram_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    
    return send_file(spectrogram_path, mimetype='image/png')

if __name__ == "__main__":
    threading.Thread(target=record_and_process, daemon=True).start()
    app.run(debug=True)