import wave
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

def plot_audio(times, signal_array, t_audio):
    plt.figure(figsize=(10, 4))
    channel = 0
    plt.plot(times, signal_array[:, channel])
    plt.ylabel(f"Channel {channel + 1}")
    plt.xlabel("Time (s)")
    plt.xlim(0, t_audio)
    plt.tight_layout()
    plt.show()

def plot_spectogram(signal_mel):
    plt.figure(figsize=(8, 4))
    plt.imshow(signal_mel[0], cmap='viridis', origin='lower', aspect='auto')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.xlabel('Time')
    plt.ylabel('Mel Frequency')
    plt.tight_layout()
    plt.show()

def initialise_output_folder():
    output_folder = "output_audio_files"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder) # delete the folder
    os.makedirs(output_folder)
    return output_folder

def save_window(count, sample_freq, window, output_folder):
    output_file = os.path.join(output_folder, f"audio_{count}.wav")
    wavfile.write(output_file, sample_freq, window.astype(np.int16))

def read_audio(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == ".aac":
        # AAC file processing
        aac_file = AudioSegment.from_file(file_path, format="aac")
        sample_freq = aac_file.frame_rate
        n_channels = aac_file.channels
        n_samples = len(aac_file)
        aac_data = np.array(aac_file.get_array_of_samples())
        signal_array = aac_data.reshape(-1, n_channels)
        # print("Sa:",signal_array,"n_S",n_samples,"s_f",sample_freq)
        return signal_array, n_samples, sample_freq
    if file_extension == ".wav":
        # WAV file processing
        obj = wave.open(file_path, "rb")
        sample_freq = obj.getframerate()
        n_samples = obj.getnframes()
        n_channels = obj.getnchannels() 
        signal_wave = obj.readframes(n_samples)
        signal_array = np.frombuffer(signal_wave, dtype=np.int16)
        signal_array = signal_array.reshape(-1, n_channels)
        return signal_array, n_samples, sample_freq
    else:
        print("Audio format not supported!")
        exit()