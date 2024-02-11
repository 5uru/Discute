from typing import List, Dict

import ollama


def chat(message: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Chat with the Ollama chatbot.

    Args: message (List[Dict[str, str]]): A list of messages in the conversation. Each message is represented as a
    dictionary with "role" and "content" keys.
    
    Returns:
        Dict[str, str]: The response message from the chatbot.

    """
    response = ollama.chat(model="qwen:7b-chat", messages=message,)
    return response["message"]


"""
messages=[
        {
            "role": "system",
            "content": "You're a useful assistant. Who sells items to tourists in Japan.  Your role is to discuss "
            "with the customer and provide precise, concrete answers.",
        },
        {"role": "user", "content": "Hello.",},
    ],
"""
