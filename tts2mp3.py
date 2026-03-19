import argparse
import os
import sys
import tempfile
import torch
import functools

# Fix for PyTorch 2.6+: Monkey-patch torch.load to default to weights_only=False
# This is required for older libraries like Coqui-TTS that load custom class configurations.
original_load = torch.load
@functools.wraps(original_load)
def patched_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = patched_load

from TTS.api import TTS
from pydub import AudioSegment

def text_to_mp3(text, output_file, model_name="tts_models/en/ljspeech/glow-tts", 
                language=None, speaker_wav=None, speaker=None, gpu=False):
    """
    Converts text to speech and saves it as an MP3 file using Coqui-TTS.
    """
    print(f"Loading model: {model_name}...")
    try:
        # Initialize TTS
        tts = TTS(model_name=model_name, progress_bar=True, gpu=gpu)
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        print("Synthesizing speech...")
        
        # Determine synthesis parameters
        kwargs = {}
        if tts.is_multi_speaker:
            if speaker_wav:
                kwargs["speaker_wav"] = speaker_wav
            elif speaker:
                kwargs["speaker"] = speaker
            else:
                # Use default speaker if none provided
                if tts.speakers:
                    kwargs["speaker"] = tts.speakers[0]

        if tts.is_multi_lingual:
            if language:
                kwargs["language"] = language
            else:
                # Use first language if none provided
                if tts.languages:
                    kwargs["language"] = tts.languages[0]

        # tts_to_file is synchronous in Coqui-TTS API
        tts.tts_to_file(text=text, file_path=temp_wav_path, **kwargs)

        print(f"Converting to MP3: {output_file}...")
        # Convert WAV to MP3 using pydub
        audio = AudioSegment.from_wav(temp_wav_path)
        audio.export(output_file, format="mp3")
        
        print(f"Success! Saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error during synthesis or conversion: {e}")
        if "Kernel size" in str(e):
            print("\nTIP: This error often occurs when the input text is too short or doesn't match the model's language.")
            if not language or language == "en":
                print("If you are using Russian text, please specify --language ru and use a multilingual or Russian model.")
        return False
    finally:
        # Clean up temporary WAV file
        if os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except:
                pass

def main():
    parser = argparse.ArgumentParser(description="Convert text to MP3 using Coqui-TTS.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to convert to speech.")
    group.add_argument("--file", type=str, help="Path to a text file to convert to speech.")
    
    parser.add_argument("--output", type=str, default="output.mp3", help="Output MP3 file path (default: output.mp3).")
    parser.add_argument("--model", type=str, default="tts_models/en/ljspeech/glow-tts", help="Coqui-TTS model name.")
    parser.add_argument("--language", type=str, help="Language code (e.g., 'en', 'ru') for multilingual models.")
    parser.add_argument("--speaker_wav", type=str, help="Path to a reference wav file for voice cloning (XTTS).")
    parser.add_argument("--speaker", type=str, help="Speaker name for multi-speaker models.")
    parser.add_argument("--gpu", action="store_true", help="Use GPU for synthesis if available.")

    args = parser.parse_args()

    input_text = ""
    if args.text:
        input_text = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            input_text = f.read()

    if not input_text.strip():
        print("Error: Input text is empty.")
        sys.exit(1)

    success = text_to_mp3(
        text=input_text, 
        output_file=args.output, 
        model_name=args.model, 
        language=args.language, 
        speaker_wav=args.speaker_wav, 
        speaker=args.speaker,
        gpu=args.gpu
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
