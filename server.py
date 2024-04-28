from io import BytesIO
import grpc
from pydub import AudioSegment
import RPC.send_audio_pb2 as your_proto
import RPC.send_audio_pb2_grpc as your_proto_grpc
from CNN.main_process import process_audio
from concurrent import futures
from log import log_received_audio

class AudioService(your_proto_grpc.AudioServiceServicer):
    def SendAudio(self, request_iterator, context):
        audio_data = b''
        for audio_chunk in request_iterator:
            audio_data += audio_chunk.data
            print(len(audio_chunk.data))

        audio = AudioSegment.from_file(BytesIO(audio_data), format="m4a")
        output_file = 'received_audio.wav'
        audio.export(output_file, format="wav")
        

        # output_file = "D:\BeerLog\CNN/audio_samples/audio1_5min.wav"

        count, time = 0, 0
        try:
            count, time = process_audio(output_file)
        except Exception as e:
            print(f"An exception of type {type(e).__name__} occurred: {e}")

        log_received_audio(count, time)
        print("Audio received")
        print(count, time)

        response = your_proto.AudioResponse(message=f"Burps:{count}, Burp period:{time}s")
        return response

class ServerStatus(your_proto_grpc.ServerStatusServicer):
    def CheckStatus(self, request, context):
        print(request)
        response = your_proto.ServerResponse(isonline=True)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    your_proto_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    your_proto_grpc.add_ServerStatusServicer_to_server(ServerStatus(), server)
    server.add_insecure_port('[::]:80')  # Specify your desired port
    server.start()
    print("Server started, listening on port 80...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()