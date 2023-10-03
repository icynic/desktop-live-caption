import torch
# pyaudiowpatch is a fork of pyaudio which supports WASAPI loopback
import pyaudiowpatch as pyaudio
import audioop
import numpy as np
import queue
import threading


class Streamer:
    """
    Record audio and put data in a queue.
    :param target_rate: Target sample rate of the audio data.
    :param frames_per_chunk: How many frames in a chunk in the queue.
    """

    def __init__(self, target_rate: int, frames_per_chunk: int):
        self.pa = pyaudio.PyAudio()
        self.device_info = None
        self.stream = None
        self.target_rate = target_rate
        self.bytes_per_chunk = frames_per_chunk * 4
        self.data_queue = queue.Queue()
        self.buffer = bytes()
        self.enqueue_event = threading.Event()

    def stream_callback(self, in_data: bytes, frame_count: int, time_info: dict, status: int) -> tuple:
        """
        Callback function to read audio.
        :param in_data: Audio data from stream.
        :param frame_count: How many frames the data contains.
        :param time_info: Stream time_info.
        :param status: Stream status.
        :return: A tuple containing audio data to output and a flag signifying whether to continue recording.
        """
        # Resample
        resampled_data, _ = audioop.ratecv(in_data, 2, 2,
                                           int(self.device_info["defaultSampleRate"]),
                                           self.target_rate, None)

        # Use buffer to form chunks which have the size specified by frames_per_chunk
        self.buffer += resampled_data
        if len(self.buffer) > self.bytes_per_chunk:
            buffered_data = self.buffer[:self.bytes_per_chunk]
            self.buffer = self.buffer[self.bytes_per_chunk:]

            # Convert audio to array and take only the left channel
            array_data = np.frombuffer(buffered_data, dtype=np.int16).reshape(-1, 2)[::2].flatten()
            # Normalize
            tensor_data = torch.from_numpy(array_data.copy()).float() / 32768.0

            # Put data and notify those who are waiting
            self.data_queue.put(tensor_data)
            self.enqueue_event.set()

        return (None, pyaudio.paContinue)

    def start_loopback_stream(self):
        """
        Open a desktop audio stream.
        When there are audio data available, call self.stream_callback in a separate thread.
        """
        self.device_info = self.pa.get_default_wasapi_loopback()
        self.stream = self.pa.open(input_device_index=self.device_info["index"],
                                   channels=self.device_info["maxInputChannels"],
                                   format=pyaudio.paInt16,
                                   rate=int(self.device_info["defaultSampleRate"]),
                                   input=True,
                                   stream_callback=self.stream_callback,
                                   frames_per_buffer=1024)

    def stop_stream(self):
        """
        Stop the current stream, if there is one.
        """
        if self.stream is not None:
            self.stream.close()
