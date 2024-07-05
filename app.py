import streamlit as st
from dotenv import load_dotenv
load_dotenv() ##to load the environment variables

import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))   ##calling the api key set up in the enviroment variable


##prompt creation for the LLM model 
prompt= """You are a Youtube video summarizer. you will be takeing the trascript text and
summarizing the entire video and providing the importatnt summary in ten bullet points.
The transcript text will be appended here. please provide the summary of the text: """


##extracting the transcript from the yt link based on the position of the "="
def extract_trascript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text= YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


##generating the summary from transcript using Gemini-pro
def generate_gemini_content(transcript_text, prompt):

    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text



##setting up the streamlit app for frontend
st.title("Youtube Trascript to detailed notes converter")
youtube_link = st.text_input("Enter youtube video link: ")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed notes"):
    transcript_text=extract_trascript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("DETAILED NOTES: ")
        st.write(summary)