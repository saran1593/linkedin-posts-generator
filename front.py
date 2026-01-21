import streamlit as st
from groq import Groq
import requests
import os

GROQ_KEY = os.getenv("GROQ_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

client = Groq(api_key=GROQ_KEY)

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

st.subheader("LinkedIn Post Generator")

topic = st.text_input("Enter your topic")

if "output" not in st.session_state:
    st.session_state.output = ""

if st.button("Generate Post"):
    if topic.strip() == "":
        st.warning("Please enter a topic")
    else:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a professional LinkedIn post for the topic: {topic}. Use some emojis to make it more engaging"
                }
            ],
        )
        st.session_state.output = response.choices[0].message.content
        st.success("Post generated!")

if st.session_state.output:
    st.write(st.session_state.output)

    if st.button("Generate Image"):
        if not st.session_state.output:
            st.warning("Generate a post first")
        else:
            payload = {
                "inputs": f"Create a LinkedIn-style image for the topic '{topic}'. "
                        f"Post content: {st.session_state.output}"
            }

            response1 = requests.post(API_URL, headers=headers, json=payload)

            if response1.status_code == 200:
                with open("output.png", "wb") as f:
                    f.write(response1.content)

                st.image("output.png", caption="Generated Image")
            else:
                st.error("Image generation failed")
