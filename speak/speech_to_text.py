from faster_whisper import WhisperModel

model_size = "large-v3"

model = WhisperModel(model_size, device="cpu", compute_type="int8")


def transcribe(language="en"):
    """
    Transcribe the audio file at the given path.
    Args:
        file_path (str): The path to the audio file.
        language (str, optional): The language of the audio file. Defaults to "en".

    Returns:
        str: The transcribed text.
    """
    segments, _ = model.transcribe("tmp_file.wave", vad_filter=True, language=language)
    segments = list(segments)  # The transcription will actually run here.
    return segments[0].text
