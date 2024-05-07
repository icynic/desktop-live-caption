# desktop-live-caption
Transcribe desktop audio/computer audio in real-time and locally (Streaming ASR), using TorchAudio and Emformer-RNNT model.

- Reimplemented stream reader using PyAudio rather than `torchaudio.io`. Thus no need for ffmpeg.
- Asynchronous data transfer via a thread-safe queue.
- Minimalist GUI to display transcriptions, built with Tkinter.

There are great models like OpenAI's Whisper to transcribe audio files, but they can't do it in real-time. 

There are some apps which transcribe microphone audio, but they can't transcribe desktop audio.

This project, however, transcribes any video or audio which is playing on your computer in real-time.

But this project isn't perfect. There is only one available model: `EMFORMER_RNNT_BASE_LIBRISPEECH`, which only supports English. And it's accuracy isn't satisfying. 

But still, it demonstrated one way to do such things.

![](https://github.com/icynic/desktop-live-caption/blob/main/Demo.gif)
