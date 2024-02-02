import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript import extract_transcript

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def fetch_transcript(video_id):
    conn = sqlite3.connect('youtube_transcripts.db')
    c = conn.cursor()
    c.execute("SELECT transcript FROM transcripts WHERE video_id = ?", (video_id,))
    transcript_text = c.fetchone()[0]
    conn.close()
    return transcript_text


def generate_notes(transcript_text, subject):
    if subject == "Physics":
        prompt = """
            Title: Detailed Physics Notes from YouTube Video Transcript

            As a physics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Highlight fundamental principles, laws, and theories discussed in the video.
            - Explain any relevant experiments, demonstrations, or real-world applications.
            - Clarify any mathematical equations or formulas introduced and provide explanations for their significance.
            - Use diagrams, illustrations, or examples to enhance understanding where necessary.

            Please provide the YouTube video transcript, and I'll generate the detailed physics notes accordingly.
        """
    elif subject == "Chemistry":
        prompt = """
            Title: Detailed Chemistry Notes from YouTube Video Transcript

            As a chemistry expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Break down chemical reactions, concepts, and properties explained in the video.
            - Include molecular structures, reaction mechanisms, and any applicable theories.
            - Discuss the significance of the discussed chemistry concepts in various contexts, such as industry, environment, or daily life.
            - Provide examples or case studies to illustrate the practical applications of the concepts discussed.

            Please provide the YouTube video transcript, and I'll generate the detailed chemistry notes accordingly.
        """
    elif subject == "Mathematics":
        prompt = """
            Title: Detailed Mathematics Notes from YouTube Video Transcript

            As a mathematics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key mathematical concepts discussed in the video.

            Your notes should:

            - Outline mathematical concepts, formulas, and problem-solving techniques covered in the video.
            - Provide step-by-step explanations for solving mathematical problems discussed.
            - Clarify any theoretical foundations or mathematical principles underlying the discussed topics.
            - Include relevant examples or practice problems to reinforce understanding.

            Please provide the YouTube video transcript, and I'll generate the detailed mathematics notes accordingly.
        """
    elif subject == "Data Science and Statistics":
        prompt = """
            Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript

            Subject: Data Science and Statistics

            Prompt:

            As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.

            Your notes should:

            Data Science:

            Explain fundamental concepts in data science such as data collection, data cleaning, data analysis, and data visualization.
            Discuss different techniques and algorithms used in data analysis and machine learning, including supervised and unsupervised learning methods.
            Provide insights into real-world applications of data science in various fields like business, healthcare, finance, etc.
            Include discussions on data ethics, privacy concerns, and best practices in handling sensitive data.
            Statistics:

            Outline basic statistical concepts such as measures of central tendency, variability, and probability distributions.
            Explain hypothesis testing, confidence intervals, and regression analysis techniques.
            Clarify the importance of statistical inference and its role in drawing conclusions from data.
            Provide examples or case studies demonstrating the application of statistical methods in solving real-world problems.

            Your notes should aim to offer a clear understanding of both the theoretical foundations and practical applications of data science and statistics discussed in the video. Use clear explanations, examples, and visuals where necessary to enhance comprehension.

            Please provide the YouTube video transcript, and I'll generate the detailed notes on Data Science and Statistics accordingly.
        """
    elif subject == "History":
        prompt = """
            Title: Comprehensive Notes on Historical Concepts from a Lecture

            Subject: History

            Prompt:

            As a history enthusiast, your task is to provide detailed notes based on the content of a historical lecture I'll provide. Assume the role of a diligent student aiming to grasp the richness of historical concepts covered in the lecture.

            Your notes should:

            Overview of Historical Periods:

            Provide a chronological overview of significant historical periods, including major events, cultural developments, and societal changes.
            Highlight key figures who played pivotal roles in shaping different eras and their contributions.
            Thematic Analysis:

            Analyze major themes that have influenced human history, such as revolutions, conflicts, technological advancements, and cultural movements.
            Discuss the impact of historical events on the political, social, and economic landscape of different regions.
            Case Studies:

            Select specific historical case studies or events to delve deeper into, providing in-depth analysis and insights.
            Explore the causes and consequences of chosen events, drawing connections to broader historical trends.
            Historiography:

            Explain the importance of historiography and how interpretations of historical events may vary over time.
            Discuss the influence of historical perspectives and biases on the study of history.
            Your notes should aim to capture the richness and complexity of historical narratives, fostering a deep understanding of the past. Utilize clear language, examples, and references to enhance the clarity and depth of your notes.

            Please provide details about the specific historical lecture, and I'll generate the comprehensive notes on History accordingly.
        """
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

def main():
    st.title("YouTube Transcript to Detailed Notes Converter")
    

    subject = st.selectbox("Select Subject:", ["Data Science and Statistics", "Physics", "Chemistry", "Mathematics", "History"])


    youtube_link = st.text_input("Enter YouTube Video Link:")


    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        # Call function to extract transcript
        transcript_text = extract_transcript(youtube_link)
        
        if transcript_text:
            st.success("Transcript extracted successfully!")
            # Generate detailed notes
            detailed_notes = generate_notes(transcript_text, subject)
            st.markdown("## Detailed Notes:")
            st.write(detailed_notes)
        else:
            st.error("Failed to extract transcript.")

if __name__ == "__main__":
    main()