import torch
import torchaudio
import streamer
import engine
import gui


def main(bundle):
    # Initialize GUI
    window = gui.run_in_another_thread()

    # Initialize inference engine
    pipeline = engine.Pipeline(bundle)
    sample_rate = bundle.sample_rate
    segment_length = bundle.segment_length * bundle.hop_length
    context_length = bundle.right_context_length * bundle.hop_length

    cacher = engine.ContextCacher(segment_length, context_length)

    # Initialize desktop stream reader
    stream_reader = streamer.Streamer(bundle.sample_rate, segment_length)
    stream_reader.start_loopback_stream()

    with torch.inference_mode():
        # End when GUI is closed
        while not window.is_closed:
            # Wait 3 seconds until stream reader put data on the queue
            stream_reader.enqueue_event.wait(3)
            stream_reader.enqueue_event.clear()

            while not stream_reader.data_queue.empty():
                chunk = stream_reader.data_queue.get()
                segment = cacher(chunk)
                transcript = pipeline.infer(segment)
                # print to console
                # print(transcript, end="", flush=True)
                # print to GUI
                window.insert_at_end(transcript)


if __name__ == '__main__':
    main(torchaudio.pipelines.EMFORMER_RNNT_BASE_LIBRISPEECH)
