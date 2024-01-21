# desktop-live-caption
Transcribe desktop audio/computer audio in real-time and locally (Streaming ASR), using TorchAudio and Emformer-RNNT model.

- Reimplemented stream reader using PyAudio rather than `torchaudio.io`. Thus no need for ffmpeg.
- Asynchronous data transfer via a thread-safe queue.
- Minimalist GUI to display transcriptions, built with Tkinter.

There are greate models like OpenAI's Whisper to transcribe audio, but they can't do it in real-time. 

And there are some apps which transcribe microphone audio, but they can't do it to desktop audio.

This project, however, transcribes any video or audio playing on your computer in real-time.


![](https://github.com/icynic/desktop-live-caption/blob/main/Demo.gif)
