import piper
import sounddevice as sd
import time

# Testing piper-tts Feb 5 2026 v1.4.1 https://github.com/OHF-Voice/piper1-gpl

if __name__ == "__main__":
    #voice_model = "voices/bmo-custom.onnx"
    voice_model = "piper/en_GB-semaine-medium.onnx"
    try:
        start_time = time.perf_counter()
        voice = piper.PiperVoice.load(voice_model)        
        end_time = time.perf_counter() - start_time
        print(f"PiperVoice.load took {end_time:.3f} seconds.")
        
        devices_info = sd.query_devices()
        print(f"[AUDIO DEBUG] sd.default.samplerate \'{sd.default.samplerate}\' Devices Info:\n{devices_info}")
        device_info = sd.query_devices(0)
        print(f"Device Name: {device_info['name']}")
        PIPER_RATE = 22050
        print(f"Default Sample Rate: {device_info['default_samplerate']} Hz PIPER_RATE {PIPER_RATE}")

        with sd.RawOutputStream(samplerate=PIPER_RATE, 
                                 channels=1, dtype='int16', 
                                 device=None, latency='low', blocksize=2048) as stream:
        #with sd.RawOutputStream(samplerate=PIPER_RATE, channels=1, dtype='int16') as stream:
            syn_config = piper.SynthesisConfig(
                volume=1,  # loudness
                length_scale=1,  # speed
                noise_scale=1.0,  # more audio variation
                noise_w_scale=1.0,  # more speaking variation
                normalize_audio=False, # use raw audio from voice
            )
            start_time = time.perf_counter()
            for audio_bytes in voice.synthesize("Hello there! This is a test, hahaha!", syn_config):
                stream.write(audio_bytes.audio_int16_bytes)
            end_time = time.perf_counter() - start_time
            print(f"PiperVoice synthesize took {end_time:.3f} seconds.")
                    
    except Exception as e:
        print(f"Audio Error: {e}")