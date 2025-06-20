import streamlit as st

from main import transcribe_audio, generate_response, generate_audio
from prompt_managements import pm

# Constants
DEFAULT_VOICE = "af_heart"
MODEL_CONTEXT = "gemma2-9b-it"
MODEL_CHAT = "mistral-saba-24b"
VOICES = {
        "American Woman 1": "af_heart",
        "American Woman 2": "af_bella",
        "American Man": "am_fenrir",
        "British Woman": "bf_emma",
        "British Man": "bm_fable"
}

def init_session_state() -> None:
    """Initialize session state variables if they don't exist"""
    if "context" not in st.session_state:
        st.session_state.context = ""
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "voice" not in st.session_state:
        st.session_state.voice = DEFAULT_VOICE

def display_chat_history() -> None:
    """Display the chat history with audio playback"""
    for msg in st.session_state.chat:
        with st.container(border=True):
            role_label = "**Me**" if msg["role"] == "me" else "**Assistant**"
            st.write(role_label)
            st.audio(msg["audio"], format="audio/wav")
            with st.expander("Show details", expanded=False):
                st.write(f"**Message:** {msg['content']}")

def format_chat_history() -> str:
    """Format the chat history for prompt context"""
    return "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in st.session_state.chat
    )

def generate_context(prompt: str, api_key: str) -> None:
    """Generate context based on a provided prompt and API key"""
    if not api_key:
        st.error("Please enter your Groq API key to generate the context.")
        return

    st.session_state.context = generate_response(prompt, MODEL_CONTEXT, api_key)

def main():
    """Main application function"""
    # App header
    st.write("# Discute")
    st.caption("Demo application for chatting with an AI assistant.")

    # API key input
    groq_api_key = st.text_input("Enter your Groq API key [Link](https://console.groq.com/home)", type="password")

    # Initialize session state
    init_session_state()

    # Context generation section
    col1, col2 = st.columns(2, border=True)

    with col1:
        st.write("**Context Prompt**")
        situation = st.text_input("Situation", placeholder="Describe the situation")
        context_prompt = pm.get_prompt("context_prompt", variables={"Situation": situation})

        if st.button("Generate Context Prompt"):
            generate_context(context_prompt, groq_api_key)

    with col2:
        st.write("**Random Context Generation**")

        if st.button("Generate Random Context", use_container_width=True):
            generate_context(pm.get_prompt("random_context"), groq_api_key)

    # Display the current context
    if st.session_state.context:
        st.write("**Context:**")
        st.info(st.session_state.context)

    # Voice selection
    st.write("**Voice Selection**")
    voice_choice = st.selectbox(
            "Select a voice",
            options=list(VOICES.keys()),
            index=0
    )
    st.session_state.voice = VOICES[voice_choice]

    # Display chat history
    display_chat_history()

    # Audio input section
    audio_col, btn_col = st.columns([3, 1])

    with audio_col:
        audio_value = st.audio_input("Record a voice message")

    with btn_col:
        # Add vertical spacing
        st.write("")
        st.write("")
        st.write("")
        if st.button("Send", use_container_width=True):
            if not audio_value:
                st.error("Please record a voice message before sending.")
            elif not groq_api_key:
                st.error("Please enter your Groq API key before sending.")
            else:
                # Process user audio
                audio_bytes = audio_value.read()
                text = transcribe_audio(audio_bytes)
                st.session_state.chat.append({"role": "me", "content": text, "audio": audio_bytes})

                # Generate AI response
                chat_history = format_chat_history()
                prompt_vars = {
                        "Context": st.session_state.context,
                        "ChatHistory": chat_history
                }

                chat_prompt = pm.get_prompt("chat_prompt", variables=prompt_vars)
                ai_response = generate_response(chat_prompt, MODEL_CHAT, groq_api_key)

                # Generate audio for AI response
                audio = generate_audio(ai_response, st.session_state.voice)

                # Add to chat history
                st.session_state.chat.append({
                        "role": "you",
                        "content": ai_response,
                        "audio": audio
                })

                # Refresh the page
                st.rerun()

    # Coach review section
    st.write("**AI Coach Review**")

    if st.button("Review and Correct", use_container_width=True):
        if not st.session_state.chat:
            st.error("No conversation to review yet.")
        elif not groq_api_key:
            st.error("Please enter your Groq API key for the review.")
        else:
            conversation = format_chat_history()
            coach_vars = {
                    "context": st.session_state.context,
                    "conversation": conversation
            }

            coach_prompt = pm.get_prompt("english_coach", variables=coach_vars)
            review = generate_response(coach_prompt, MODEL_CHAT, groq_api_key)

            st.write("**Coach Review:**")
            st.info(review)

if __name__ == "__main__":
    main()