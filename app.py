# import streamlit as st
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi
# from deep_translator import GoogleTranslator


# # Set your API key
# genai.configure(api_key="AIzaSyAudJfCh_7rfLbhYIwbshlSc3TbLjnqoP0")

# # Prompt template
# base_prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video 
# and providing the important summary in points within 500 words. Please provide the summary of the text given here: """

# def get_difficulty_prompt(difficulty):
#     if difficulty == "Simple":
#         return base_prompt + " Use simple language that is easy to understand."
#     elif difficulty == "Medium":
#         return base_prompt + " Use a moderate level of language complexity."
#     elif difficulty == "Hard":
#         return base_prompt + " Use advanced language and include technical terms if applicable."
#     else:
#         return base_prompt

# def extract_video_id(youtube_url):
#     try:
#         if "v=" in youtube_url:
#             return youtube_url.split("v=")[1].split("&")[0]
#         elif "youtu.be/" in youtube_url:
#             return youtube_url.split("youtu.be/")[1].split("?")[0]
#     except:
#         return None

# def fetch_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         return " ".join([segment["text"] for segment in transcript_list])
#     except Exception as e:
#         st.error(f"Transcript Error: {e}")
#         return None


# def generate_summary(transcript_text, prompt):
#     try:
#         model = genai.GenerativeModel("text-bison-001")  # Update with the correct model name
#         response = model.generate_content(prompt + transcript_text)
#         return response.text
#     except Exception as e:
#         return f"❌ Failed to generate content: {e}"

# def translate_text(text, target_lang):
#     try:
#         translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
#         return translated
#     except Exception as e:
#         return f"❌ Translation failed: {e}"


# def main():
#     st.set_page_config(
#         page_title="YouTube Transcript Converter",
#         page_icon="📹",
#         layout="centered"
#     )

#     st.title("🎬 YouTube Transcript to Detailed Notes Converter")
#     youtube_link = st.text_input("🔗 Enter YouTube Video Link:")

#     if youtube_link:
#         video_id = extract_video_id(youtube_link)
#         if video_id:
#             st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

#             languages = {
#                 "English": "en", "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh-cn",
#                 "Japanese": "ja", "Korean": "ko", "Hindi": "hi", "Urdu": "ur", "Telugu": "te", "Kannada": "kn"
#             }
#             target_language = st.selectbox("🌐 Select the target language for the summary:", list(languages.keys()))
#             difficulty = st.selectbox("🧠 Select the difficulty level of the summary:", ["Simple", "Medium", "Hard"])

#             if st.button("📝 Get Summary Notes"):
#                 transcript = fetch_transcript(video_id)
#                 if transcript:
#                     with st.spinner("⏳ Generating summary..."):
#                         prompt = get_difficulty_prompt(difficulty)
#                         summary = generate_summary(transcript, prompt)

#                     if summary:
#                         translated = translate_text(summary, languages[target_language])

#                         st.markdown("## 📄 Summarized Notes:")
#                         st.write(translated)

#                         st.download_button(
#                             label="⬇️ Download Summary",
#                             data=translated,
#                             file_name="summary.txt",
#                             mime="text/plain"
#                         )
#         else:
#             st.error("❌ Invalid YouTube URL format.")

# if __name__ == "__main__":
#     main()

from flask import Flask, render_template, request, jsonify, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyAP7MfrN5yShyfHIX1VVxZqITTLN7HCt20")

# Base Prompt
base_prompt = """You are a YouTube video summarizer. Create a detailed summary with proper headings and bullet points (under 500 words). 
Format the output with Markdown-style headings (# for main headings, ## for subheadings). 
Include emojis where appropriate to make it more engaging."""

def get_difficulty_prompt(difficulty):
    if difficulty == "Simple":
        return base_prompt + " Use simple and easy language with basic explanations."
    elif difficulty == "Medium":
        return base_prompt + " Use moderately technical language with some explanations."
    elif difficulty == "Hard":
        return base_prompt + " Use technical and advanced terminology with minimal explanations."
    else:
        return base_prompt

def extract_video_id(url):
    try:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
    except:
        return None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([segment["text"] for segment in transcript])
    except Exception as e:
        return f"Transcript Error: {e}"

def generate_summary(prompt, transcript):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat()
        response = chat.send_message(prompt + "\n\nTranscript:\n" + transcript)
        return response.text
    except Exception as e:
        return f"❌ Failed to generate summary: {e}"

def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"❌ Translation failed: {e}"

def create_pdf(html_content):
    pdf = FPDF()
    pdf.add_page()
    
    # Add DejaVu Sans font for Unicode support
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    
    # Convert HTML to plain text with basic formatting
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Add title
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, 'YouTube Transcript to Detailed Notes Converter', 0, 1, 'C')
    pdf.ln(10)
    
    # Add content
    pdf.set_font('DejaVu', '', 12)
    
    for element in soup.find_all(['h1', 'h2', 'p', 'li']):
        if element.name == 'h1':
            pdf.set_font('DejaVu', 'B', 14)
            pdf.cell(0, 10, element.get_text(), 0, 1)
            pdf.set_font('DejaVu', '', 12)
        elif element.name == 'h2':
            pdf.set_font('DejaVu', 'B', 12)
            pdf.cell(0, 10, element.get_text(), 0, 1)
            pdf.set_font('DejaVu', '', 12)
        else:
            pdf.multi_cell(0, 10, element.get_text())
        pdf.ln(5)
    
    # Save to bytes buffer
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

def format_summary_content(content):
    # Convert markdown to HTML
    html_lines = []
    in_list = False
    
    for line in content.split('\n'):
        if line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:].strip()}</li>')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<p>&nbsp;</p>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{line.strip()}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        target_language = request.form.get('target_language')
        difficulty = request.form.get('difficulty')
        
        video_id = extract_video_id(youtube_link)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL format.'})
        
        transcript = fetch_transcript(video_id)
        if "Error" in transcript:
            return jsonify({'error': transcript})
        
        prompt = get_difficulty_prompt(difficulty)
        summary = generate_summary(prompt, transcript)
        translated = translate_text(summary, target_language)
        
        return jsonify({
            'thumbnail': f'http://img.youtube.com/vi/{video_id}/0.jpg',
            'summary': translated,
            'video_id': video_id
        })
    
    return render_template('index.html')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    content = request.form.get('content')
    formatted_content = format_summary_content(content)
    pdf_bytes = create_pdf(formatted_content)
    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name='youtube_summary.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)