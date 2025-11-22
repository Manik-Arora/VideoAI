import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from config import GEMINI_API_KEY

from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

def convert_text_to_speech(text, folder):
    client = genai.Client(api_key = GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore',
                    )
                )
            ),
        )
    )

    data = response.candidates[0].content.parts[0].inline_data.data

    # Create audio file path
    audio_file_path = os.path.join(f"user_uploads/{folder}", "audio.wav")

    # Saves the file in the same folder
    wave_file(audio_file_path, data)

    print(f"{audio_file_path}: A new audio file was saved successfully!")
