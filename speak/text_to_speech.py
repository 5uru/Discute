import scipy
from bark import SAMPLE_RATE
from transformers import AutoProcessor, BarkModel


model_name = "suno/bark-small"
processor = AutoProcessor.from_pretrained(model_name)
model = BarkModel.from_pretrained(model_name)


def generate_audio(text, name):
    """
   Generates audio from the given text.

   Args:
       text (str): The text to convert to audio.
       name (str): The name of the audio file.

   Returns:
       numpy.ndarray: The generated audio as a NumPy array.
   """
    voice_preset = "v2/en_speaker_1"
    inputs = processor(text, voice_preset=voice_preset)

    audio_array = model.generate(**inputs, pad_token_id=100)
    audio_array = audio_array.cpu().numpy().squeeze()
    output_path = f"../output/{name}.wav"
    scipy.io.wavfile.write(output_path, rate=SAMPLE_RATE, data=audio_array)
    return audio_array


text = "Hello World! How are you? I'm fine, thank you. And you?"

audio = generate_audio(text, "hello_world")
