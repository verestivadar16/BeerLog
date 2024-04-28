BeerLog: Audio Analysis App
# Audio Analysis Application

This repository contains a client-server application for audio processing and analysis using gRPC for communication between a Flutter client and a Python server. The server performs audio analysis using a CNN (Convolutional Neural Network) model trained on audio data.

## Components

### 1. Server (Python)

#### Server Setup

- The server is implemented in Python using gRPC for communication.
- The `AudioService` class handles audio data reception and processing.
- Audio is received in chunks via gRPC and then converted from the M4A format to WAV.
- Processed audio data is analyzed using the `CNNNetwork` model to detect specific patterns (like burps) and measure their occurrence over time.

#### Dependencies

- `grpc`: For setting up the gRPC server and defining the service interfaces.
- `pydub`: For audio file manipulation (conversion, segmentation).
- `torch`: For the CNN model used in audio analysis.
- `wave`, `os`, `shutil`: For general file I/O and system operations.

### 2. Flutter Client (Dart)

#### Client Setup

- The Flutter client app provides an interface for recording audio and sending it to the server for analysis.
- Utilizes the `record` and `audioplayers` packages for audio recording and playback.
- gRPC is used to communicate with the Python server (`RpcService`) for sending and receiving audio data.

#### Dependencies

- `record`: For audio recording functionality in Flutter.
- `audioplayers`: For audio playback within the Flutter app.
- `grpc`: Dart package for gRPC communication.

### 3. CNN Model (Python)

#### CNN for Audio Analysis

- The CNN model (`CNNNetwork`) defined in Python using PyTorch is used for audio pattern recognition.
- Trained on audio data to identify specific features like burp occurrences.

## Usage

### Server Setup

- Run the Python server (`server.py`) to start the gRPC server listening on port 80.
- Ensure all required dependencies (`grpc`, `pydub`, `torch`, etc.) are installed.

### Flutter Client

- Run the Flutter app (`main.dart`) on an emulator or physical device.
- The app allows recording audio, which can be sent to the server for analysis via gRPC.

### CNN Model

- The CNN model (`CNNNetwork`) is used within the server to process audio data.
- The model is trained using the `UrbanSoundDataset` and can be fine-tuned as needed.

## Additional Scripts

- `plot_audio`, `plot_spectogram`: Helper functions for visualizing audio data.
- `initialise_output_folder`, `save_window`, `read_audio`: Utility functions for audio file operations.
- `train.py`, `inference.py`: Scripts for training and evaluating the CNN model.

## Requirements

- Python 3.6+
- Dart/Flutter SDK
- PyTorch (for CNN model training)
- gRPC (Python and Dart packages)
- Additional Python libraries (`pydub`, `torch`, `torchaudio`, `wave`, `matplotlib`, `numpy`, etc.)

## Future Improvements

- Enhance the CNN model with more training data for better accuracy.
- Implement real-time audio analysis and feedback in the Flutter client.
- Improve error handling and scalability of the gRPC server.

## Contributors

- [Veres Tivadar](https://github.com/verestivadar16) - GitHub Profile

