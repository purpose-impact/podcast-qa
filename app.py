import streamlit as st
import anthropic
from anthropic import AI_PROMPT, HUMAN_PROMPT
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

st.title("🎙️ Podcast Bot", anchor=False)
st.markdown("Upload a podcast transcript to be summarized automatically, then ask more questions to clarify!")
uploaded_file = st.file_uploader("Upload transcript", type=("txt"))

def run_completion_and_print():
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response = ""
        for data in client.completions.create(
            prompt=" ".join([m["content"] for m in st.session_state.messages]),
            stop_sequences=[HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=1000,
            stream=True,
        ):
            response += data.completion
            response_placeholder.markdown(response + "▌")
        response_placeholder.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

if uploaded_file and anthropic_api_key:
    client = anthropic.Client()
    transcript = uploaded_file.read().decode()

    # Initialize chat history
    ran_summary = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Summarize uploaded text initially
        summarize_prompt = (
            f"Here's a podcast transcript:\n\n<transcript>{transcript}</transcript>\n\n"
            "Can you give me a brief summary?"
        )
        st.session_state.messages = [{"role": "user", "content": f"{HUMAN_PROMPT} {summarize_prompt}n\n{AI_PROMPT}"}]
        run_completion_and_print()
        ran_summary = True

    # Display chat messages from history on app rerun
    start_idx = 2 if ran_summary else 1
    for message in st.session_state.messages[start_idx:]:
        with st.chat_message(message["role"]):
            content = message["content"]
            if message["role"] == "user":
                content = message["content"][len(f"{HUMAN_PROMPT} ") : -len(f"{AI_PROMPT} ")]
            st.markdown(content)

    # Accept user input
    if prompt := st.chat_input("Ask a question about the podcast"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": f"{HUMAN_PROMPT} {prompt}{AI_PROMPT} "})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        run_completion_and_print()