from transformers import AutoTokenizer, T5ForConditionalGeneration

tokenizer = AutoTokenizer.from_pretrained("grammarly/coedit-large")
model = T5ForConditionalGeneration.from_pretrained("grammarly/coedit-large")


def process_text(text, task_type):
    """
    Process the given text based on the task type.

    Args:
        text (str): The text to process.
        task_type (str): The type of task to perform on the text.

    Returns:
        str: The processed text.
    """
    task_prefixes = {
        "grammar_correction": "Fix grammatical errors in this sentence:",
        "coherence_correction": "Make this text coherent:",
        "rewrite_text": "Rewrite to make this easier to understand:",
    }
    input_text = f"{task_prefixes[task_type]} {text}"  # prepend the task prefix
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=1000)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def grammar_coherence_correction(text):
    """
    Combine grammar correction, coherence correction, and text rewriting.

    Args:
        text (str): The text to process.

    Returns:
        dict: A dictionary containing the score, grammar corrected text, coherence corrected text, and rewritten text.
    """
    grammar_corrected = process_text(text, "grammar_correction")
    coherence_corrected = process_text(grammar_corrected, "coherence_correction")
    rewritten = process_text(coherence_corrected, "rewrite_text")
    # calculate the difference between texts
    score = (
        len(set(rewritten.split()) - set(text.split()))
        + len(set(coherence_corrected.split()) - set(text.split()))
        + len(set(grammar_corrected.split()) - set(text.split()))
    )
    # Percentage of words changed
    score = score / len(text.split()) * 100
    return {
        "score": score,
        "grammar_corrected": grammar_corrected,
        "coherence_corrected": coherence_corrected,
        "rewritten": rewritten,
    }
