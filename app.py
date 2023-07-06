import streamlit as st
import anthropic

anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

st.title("📝 File Q&A with Anthropic")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and anthropic_api_key:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client()

    st.write("### Answer")
    ans_box = st.empty()
    
    stream = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",
        max_tokens_to_sample=1000,
        stream=True,
    )
    ans = ""
    for data in stream:
        ans += data.completion
        ans_box.markdown(ans)
    