import torch
import os
import torchaudio
import time

from urbansounddataset import UrbanSoundDataset
from torch.utils.data import DataLoader
from inference import inference
from cnn import CNNNetwork
from torch import nn

BATCH_SIZE = 128
EPOCHS = 30
LEARNING_RATE = 0.000076
# 0.000077
ANNOTATIONS_FILE = os.path.join('..', 'UrbanSound8K', 'metadata', 'UrbanSound8K_train.csv') # the train dataset's csv
AUDIO_DIR = os.path.join('..', 'UrbanSound8K', 'audio')
SAMPLE_RATE = 48000
NUM_SAMPLES = 15360


def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return train_dataloader


def train_single_epoch(model, data_loader, loss_fn, optimiser, device):
    for input, target in data_loader:
      
        input, target = input.to(device), target.to(device)
        
        # calculate loss
        prediction = model(input)
        loss = loss_fn(prediction, target)

        # backpropagate error and update weights
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

    print(f"loss: {loss.item()}")


def train(model, data_loader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        train_single_epoch(model, data_loader, loss_fn, optimiser, device)
        print("---------------------------")
    print("Finished training")


if __name__ == "__main__":
    # print("Torchaudio Version:", torchaudio.__version__)
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Using {device}")

    # instantiating our dataset object and create data loader
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
                            device)
    
    train_dataloader = create_data_loader(usd, BATCH_SIZE)

    # construct model and assign it to device
    cnn = CNNNetwork().to(device)
    print(cnn)

    # initialise loss funtion + optimiser
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=LEARNING_RATE)
    

    file_name = "cnnnet4.pth"
    start_time = time.time()
    # train model
    accuracy = 0
    while accuracy < 99:
        train(cnn, train_dataloader, loss_fn, optimiser, device, EPOCHS)
        torch.save(cnn.state_dict(), file_name)
        accuracy = inference(file_name)


    end_time = time.time()
    runtime_seconds = end_time - start_time
    print(f"Runtime: {runtime_seconds} seconds")
    runtime_minutes = runtime_seconds / 60
    print(f"Runtime: {runtime_minutes:.2f} minutes")


    print("Ieal loss to be under 0.35")

    print("You can test the recognition rate with the Inference file")

    print("The success of recognition also depends on the random values generated!")

    # save model
  
    # torch.save(cnn.state_dict(), file_name)
    print(f"Trained feed forward net saved at {file_name}")