:

🎯 Project Aim

Build an AI-powered YouTube Transcript Summarizer web app using Flask (Python backend), Google Gemini API, and Deep Translator API,
where a user can enter a YouTube link and receive a detailed, translated summary in real-time.
Additionally, the summary can be downloaded as a PDF with proper headings and bullet points.

⚙️ Modules Used and Their Roles
Module	Purpose
Flask	Web framework — creates routes (/ and /download_pdf) and runs the web server
youtube_transcript_api	Fetches the transcript of a YouTube video by video ID
deep_translator	Translates AI-generated summaries into the user-selected target language
google.generativeai	Calls Google Gemini API to generate a summarized text from the transcript
FPDF	Converts HTML/Markdown-formatted summaries into a PDF
io (BytesIO)	Handles in-memory PDF files for download
BeautifulSoup	Parses AI-generated HTML content for PDF formatting
re (Regex)	Handles text cleaning if required
render_template	Loads front-end HTML (index.html) for the user interface
jsonify	Converts Python dictionaries into JSON responses for AJAX calls
send_file	Sends generated PDFs to the user as downloadable files
🧠 Workflow — Step-by-Step
1) Start the Flask Server

The app runs at http://0.0.0.0:5000

debug=True during development for live reloads

Supports multiple concurrent users

2) User Opens the Web Page (/ route)

Flask renders index.html with:

Input field for YouTube link

Dropdown for target language

Dropdown for difficulty level (Simple / Medium / Hard)

Submit button to generate summary

3) User Submits a YouTube Link

JavaScript sends a POST request to / with the payload:

{
  "youtube_link": "<URL>",
  "target_language": "<language>",
  "difficulty": "<difficulty>"
}

4) Backend Processing

Extract Video ID:

extract_video_id() handles URLs in both youtu.be and youtube.com/watch?v= formats

Fetch Transcript:

fetch_transcript(video_id) uses youtube_transcript_api

Generate Summary via Gemini API:

get_difficulty_prompt(difficulty) adjusts AI prompt based on difficulty

generate_summary(prompt, transcript) calls Gemini API to produce a detailed, structured summary

Translate Summary:

translate_text(summary, target_language) translates AI output to the selected language

5) Return JSON Response to Frontend

Example JSON response:

{
  "thumbnail": "http://img.youtube.com/vi/<video_id>/0.jpg",
  "summary": "<translated_summary>",
  "video_id": "<video_id>"
}

6) Optional PDF Download (/download_pdf route)

format_summary_content(content) converts AI Markdown to HTML

create_pdf(html_content) generates a PDF using FPDF + DejaVuSans font

Sends the PDF as a downloadable file:

send_file(
    pdf_bytes,
    as_attachment=True,
    download_name='youtube_summary.pdf',
    mimetype='application/pdf'
)

🔁 Error Handling
Case	Response
Invalid YouTube URL	{'error': 'Invalid YouTube URL format.'}
Transcript Fetch Failure	{'error': 'Transcript Error: <details>'}
Gemini API Failure	Returns a message like ❌ Failed to generate summary: <details>
Translation Failure	Returns a message like ❌ Translation failed: <details>
🧩 Summary of Workflow

✅ Frontend → User inputs YouTube link, target language, difficulty
✅ Flask Backend → Processes input, extracts video ID, fetches transcript
✅ Google Gemini API → Generates structured summary
✅ Deep Translator → Translates summary into chosen language
✅ BeautifulSoup + FPDF → Formats and generates downloadable PDF
✅ Frontend → Displays translated summary with thumbnail and download option

📌 Key Features

Supports any YouTube video with English transcripts

Provides multi-language translation for summaries

Generates structured summaries with headings, subheadings, and bullet points

Allows PDF download of summaries

Adjustable difficulty levels: Simple / Medium / Hard
