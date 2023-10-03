# desktop-live-caption
Transcribe desktop audio/computer audio in real-time and locally (Streaming ASR), using TorchAudio and Emformer-RNNT model.

- Reimplemented stream reader using PyAudio rather than `torchaudio.io`. Thus no need for ffmpeg.
- Asynchronous data transfer via a thread-safe queue.
- Minimalist GUI to display transcriptions, built with Tkinter.

![](https://github.com/icynic/desktop-live-caption/blob/main/Demo.gif)
