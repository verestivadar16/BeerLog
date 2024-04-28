import torch
import numpy as np

from CNN.load_to_cnn import LoadToNet
from CNN.cnn import CNNNetwork
from CNN.functions import read_audio
from CNN.functions import initialise_output_folder # to extract the recognized burps
from CNN.functions import save_window

SAMPLE_RATE = 48000
NUM_SAMPLES = 15360
BATCH_SIZE = 128

class_mapping = [
    "other",
    "burp",
]

def process_audio(path):
    cnn = CNNNetwork()
    state_dict = torch.load("CNN/cnnnet4.pth", map_location='cpu')
    cnn.load_state_dict(state_dict)
    cnn.eval()
    path = "D:\BeerLog\Oct 3, 2.16 PM_.aac"
    signal_array, n_samples, sample_freq = read_audio(path)
    t_audio = n_samples / sample_freq
    output_folder = initialise_output_folder() # to extract the recognized burps

    sec = 2     #window size (sec*48000 frames)
    skip_size = int(sample_freq*sec)  
    sec = 0.05        
    scan_size = int(sample_freq*sec)  
    sec = 0.32    
    sample_size = int(sample_freq*sec) 
    sec = 0.02       
    back_size = int(sample_freq*sec) 

    count = 0
    start_time = 0
    end_time = 0
    ok=False

    i=0
    while i <= len(signal_array):
        window = signal_array[i:i + scan_size]
        max_value = np.max(np.abs(window))
        if (max_value >= 4000 and max_value <=6300):
            window = signal_array[i - back_size:i + sample_size - back_size]

            tmp = torch.tensor(window)
            tmp = tmp.to(torch.float32)
            tmp = tmp / torch.max(torch.abs(tmp))
            signal = torch.rot90(tmp, k=1)

            signal_obj = LoadToNet(signal, 
                               SAMPLE_RATE,
                               SAMPLE_RATE, 
                               NUM_SAMPLES)
            signal_mel = signal_obj.__getitem__()
            signal = signal_mel.unsqueeze(0)
           
            with torch.no_grad():
                predictions = cnn(signal)
                predicted_index = predictions[0].argmax(0)
                predicted = class_mapping[predicted_index]

                if(predicted == class_mapping[1]): #burp
                    count = count+1
                    if(ok == False):
                        start_time=i
                        ok=True
                    end_time = i
                    save_window(count, sample_freq, window, output_folder) # to extract the recognized burps

            i += skip_size

        i += scan_size

    t_audio = (end_time-start_time) / sample_freq

    if(count !=0):
         return count, round(t_audio/count,2)
    else:
         return 0,0

if __name__ == "__main__":

    file_name = "D:\BeerLog\CNN/audio_samples/audio1_5min.wav"
    count, burps_period = process_audio(file_name)

    print("Number of burp's:",count)
    if count != 0:
      print("Avg time between burp's:", round(burps_period,2),"sec" )
