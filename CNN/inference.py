import torch
import torchaudio
import os
import pandas as pd

from cnn import CNNNetwork
from urbansounddataset import UrbanSoundDataset
ANNOTATIONS_FILE = os.path.join('..', 'UrbanSound8K', 'metadata', 'UrbanSound8K_test.csv') # the test dataset's csv

AUDIO_DIR = os.path.join('..', 'UrbanSound8K', 'audio')
SAMPLE_RATE = 48000
NUM_SAMPLES = 15360

class_mapping = [
    "other",
    "burp",
]
length = len(pd.read_csv(ANNOTATIONS_FILE))


def predict(model, input, target, class_mapping):
    model.eval()
    with torch.no_grad():
        predictions = model(input)
        print(predictions)
        # Tensor (1, 2) -> [ [0.1, 0.9] ]
        predicted_index = predictions[0].argmax(0)
        predicted = class_mapping[predicted_index]
        expected = class_mapping[target]
    return predicted, expected
def inference(file_name):
    # load back the model
    cnn = CNNNetwork()
    state_dict = torch.load(file_name)
    cnn.load_state_dict(state_dict)

    # load urban sound dataset
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )

    usd = UrbanSoundDataset(ANNOTATIONS_FILE,
                            AUDIO_DIR,
                            mel_spectrogram,
                            SAMPLE_RATE,
                            NUM_SAMPLES,
                            "cpu")

    count = 0
    count2 = 0
    # get a sample from the urban sound dataset for inference

    for i in range(length):

        input, target = usd[i][0], usd[i][1] # [batch size, num_channels, fr, time]
        
        input.unsqueeze_(0)

        # make an inference
        predicted, expected = predict(cnn, input, target,
                                    class_mapping)
        if predicted == expected:
            count = count+1
        if predicted != expected:
            count2 = count2+1
        print(f"Predicted: '{predicted}', expected: '{expected}' '{i}'")
    accuracy = round(count/length,2)*100
    print("Number of miss:",count2,"of:",length)
    print(f"Accuracy: {accuracy}%")
    print("Ideal accuracy is over 98%")
    return accuracy

if __name__ == "__main__":
    _ = inference("cnnnet1.pth")
   
 