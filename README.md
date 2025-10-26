# 🎯 Project Aim

Build an **AI-powered YouTube Transcript Summarizer Web App** using **Flask (Python backend)** and **Google Gemini API**,  
where a user can enter a YouTube video link, get a detailed summary of the video, translate it into any language, and download it as a PDF.

---

## ⚙️ Modules Used and Their Roles

| Module                   | Purpose                                                                                                   |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| Flask                     | Web framework — handles routing (`/` and `/download_pdf`) and runs the web server                          |
| youtube_transcript_api    | Fetches the transcript of a YouTube video using its video ID                                              |
| deep_translator           | Translates the AI-generated summary into the target language specified by the user                        |
| google.generativeai       | Connects to Google Gemini API to generate AI-based video summaries                                        |
| fpdf                      | Creates downloadable PDF files from the formatted summary content                                         |
| io.BytesIO                | Stores the generated PDF in memory for sending to the user without saving on disk                         |
| bs4 (BeautifulSoup)       | Parses HTML content generated from markdown to prepare it for PDF creation                                 |
| re                        | Handles text cleaning or pattern matching if required                                                     |
| render_template           | Loads the frontend HTML (`index.html`) for user interaction                                               |
| request                   | Retrieves POST form data such as YouTube link, target language, and difficulty level                       |
| jsonify                   | Returns JSON responses to the frontend, e.g., video thumbnail, summary, and video ID                      |
| send_file                 | Sends the generated PDF as a downloadable file to the user                                               |

---

## 🧠 Workflow — Step-by-Step

### 1) Start the Flask Server
- The app runs at `http://0.0.0.0:5000`  
- `debug=True` → shows errors during development  

### 2) User Opens the Web Page (`/` route)
- Flask renders `index.html`, which contains:
  - Input box for the YouTube video link
  - Dropdown for target language selection
  - Dropdown for difficulty level selection
  - Button to generate summary

### 3) User Submits Video Link
- **Frontend sends a POST request** with YouTube URL, target language, and difficulty.
- **Backend Extracts Video ID**:
  - Handles URLs in formats like:
    - `https://www.youtube.com/watch?v=<video_id>`
    - `https://youtu.be/<video_id>`

### 4) Fetch Video Transcript
- Uses `YouTubeTranscriptApi` to retrieve the transcript
- Joins all text segments into a single string for AI processing
- If transcript fails, returns an error JSON to the frontend

### 5) Generate Summary Using Gemini API
- Prepares a prompt based on the selected difficulty:
  - **Simple** → easy-to-understand language
  - **Medium** → moderately technical
  - **Hard** → advanced technical language
- Sends the transcript + prompt to **Google Gemini API**
- Receives an AI-generated summary in Markdown format

### 6) Translate Summary (Optional)
- Uses `deep_translator` to translate summary into the user-selected target language
- Supports multiple languages (English, Hindi, Telugu, etc.)

### 7) Format Summary for PDF
- Converts Markdown headings and bullet points to HTML using `BeautifulSoup` and custom logic
- Handles headings (`h1`, `h2`), paragraphs (`p`), and lists (`ul/li`)

### 8) Create PDF
- Uses `FPDF` to:
  - Add a title
  - Render headings, paragraphs, and bullet points
  - Generate a downloadable PDF stored in memory (`BytesIO`)
- PDF is returned via `/download_pdf` route

### 9) Frontend Displays Results
- Shows:
  - Video thumbnail (`http://img.youtube.com/vi/<video_id>/0.jpg`)
  - Translated AI-generated summary
  - Button to download summary PDF

---

## 🔁 Error Handling

| Case                        | Response                                                        |
|------------------------------|----------------------------------------------------------------|
| Invalid YouTube URL           | `{'error': 'Invalid YouTube URL format.'}`                     |
| Transcript fetch fails        | `{'error': 'Transcript Error: <reason>'}`                     |
| Translation fails             | `❌ Translation failed: <reason>`                               |
| Gemini API fails              | `❌ Failed to generate summary: <reason>`                      |

---

## 🧩 Summary

✅ **Frontend** → sends YouTube URL, language, difficulty  
✅ **Flask Backend** → extracts video ID, fetches transcript, prepares prompt  
✅ **Gemini API** → generates AI summary  
✅ **deep_translator** → translates summary  
✅ **BeautifulSoup + FPDF** → formats and creates downloadable PDF  
✅ **Flask** → returns JSON and PDF to frontend  

---

## 📌 Interview Preparation Notes

- Explain **how Flask handles routes** and form submission
- Explain **video ID extraction logic** for different YouTube URL formats
- Show **Gemini API integration** and prompt engineering
- Highlight **Markdown to HTML conversion** logic
- Demonstrate **PDF generation** using FPDF
- Discuss **error handling** in web apps
- Emphasize **workflow: Frontend → Backend → API → Frontend**

