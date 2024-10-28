import os
import time
from typing import Any
import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from transformers import pipeline
from PIL import Image

# Load environment variables
load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


st.markdown("""
    <style>
        /* Background and Font */
        body {
            background-color: #f3e5f5;
            font-family: 'Comic Sans MS', cursive;
            color: #4a148c;
        }

        /* Header */
        .stApp header, .stApp [data-testid="stHeader"] {
            background-color: #7b1fa2;
            color: white;
        }

        /* Sidebar styling */
        .stSidebar {
            background-color: #ce93d8;
        }

        /* Button styling */
        .stButton button {
            background-color: #ba68c8;
            color: white;
            border-radius: 10px;
            border: none;
        }

        .stButton button:hover {
            background-color: #ab47bc;
            color: white;
            transition: 0.3s;
        }

        /* Progress bar */
        .stProgress > div > div {
            background-color: #7b1fa2;
        }

        /* Expander text and border */
        .st-expander {
            background-color: #e1bee7;
            border: 1px solid #7b1fa2;
            border-radius: 8px;
            padding: 10px;
        }

        /* Custom font for headings */
        .stApp h1, .stApp h2, .stApp h3 {
            font-family: 'Poppins', sans-serif;
            color: #6a1b9a;
        }
    </style>
""", unsafe_allow_html=True)


# Progress Bar Function
def progress_bar(duration: int) -> None:
    progress_text = "Please wait, generative models hard at work 🐾"
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(duration):
        time.sleep(0.04)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()


# Main App
def main() -> None:
    st.set_page_config(page_title="Cute Image to Story Converter", page_icon="🌸")
    st.sidebar.title("🌸 Cute AI App by @Gurpreet Kaur 🌸")
    st.sidebar.write("Upload an image to get a custom story and audio!")

    st.title("Welcome to the Cute Image-to-Story Converter!")

    uploaded_file = st.file_uploader("Choose an adorable image to upload", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image 🌈", use_column_width=True)
        progress_bar(100)

        scenario = generate_text_from_image(image)
        story = generate_story_from_text(scenario)
        audio_file_path = generate_speech_from_text(story)

        with st.expander("📜 Generated Image Scenario"):
            st.write(scenario)
        with st.expander("📖 Generated Short Story"):
            st.write(story)

        if audio_file_path:
            st.audio(audio_file_path)


if __name__ == "__main__":
    main()
