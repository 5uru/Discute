from gtts import gTTS


def generate_audio(text):
    """
   Generates audio from the given text.

   Args:
       text (str): The text to convert to audio.

   Returns:
       numpy.ndarray: The generated audio as a NumPy array.
   """
    inputs = gTTS(text=text, lang="en", slow=False)

    inputs.save("tmp_file.wav")

    # transform wav to bytes
    with open("tmp_file.wav", "rb") as file:
        audio_bytes = file.read()
    return audio_bytes
