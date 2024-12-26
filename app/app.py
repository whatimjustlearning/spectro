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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log')  # Log to file
    ]
)
logger = logging.getLogger(__name__)

# Add a startup message to verify logging works
logger.info("Application starting...")

import os
print("Current working directory:", os.getcwd())

app = Flask(__name__, template_folder='/home/spectro/app/templates')
UPLOAD_FOLDER = 'uploads'
TMP_FOLDER = 'tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TMP_FOLDER, exist_ok=True)

def record_and_process():
    try:
        logger.info("Initializing AudioProcessor...")
        processor = AudioProcessor()
        processor.start_stream()
        logger.info("Audio stream started successfully")
        
        while True:
            frames = []
            logger.info("Recording 2 seconds of audio...")
            for _ in range(int(processor.RATE / processor.CHUNK * 2)):
                try:
                    data = processor.read_chunk()
                    frames.append(data)
                except Exception as e:
                    logger.error(f"Error reading audio chunk: {e}")
                    raise
            
            # Save the recorded frames as a WAV file
            filename = os.path.join(TMP_FOLDER, 'current.wav')
            logger.info(f"Saving WAV file to {filename}")
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(processor.CHANNELS)
                wf.setsampwidth(processor.p.get_sample_size(processor.FORMAT))
                wf.setframerate(processor.RATE)
                wf.writeframes(b''.join(frames))
            
            logger.info("Generating spectrogram...")
            generate_spectrogram(filename)
            logger.info("Spectrogram generated successfully")
            
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Error in record_and_process: {e}", exc_info=True)
        raise

def generate_spectrogram(wav_file):
    try:
        logger.info(f"Reading WAV file: {wav_file}")
        sample_rate, data = scipy.io.wavfile.read(wav_file)
        
        if len(data.shape) == 2:
            logger.info("Converting stereo to mono")
            data = data.mean(axis=1)
        
        logger.info("Creating spectrogram plot")
        plt.figure(figsize=(10, 4))
        plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='viridis')
        plt.axis('off')
        
        output_path = os.path.join(UPLOAD_FOLDER, 'spectrogram.png')
        logger.info(f"Saving spectrogram to {output_path}")
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        logger.info("Spectrogram saved successfully")
    except Exception as e:
        logger.error(f"Error generating spectrogram: {e}", exc_info=True)
        raise

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
    logger.info("Starting recording thread...")
    recording_thread = threading.Thread(target=record_and_process, daemon=True)
    recording_thread.start()
    logger.info("Recording thread started")
    app.run(debug=True, host='0.0.0.0', port=5000)