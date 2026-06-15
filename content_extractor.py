from urllib.parse import urlparse, parse_qs
from pypdf import PdfReader
from docx import Document
from youtube_transcript_api import YouTubeTranscriptApi


def extract_from_txt(file_path):
    try:
        with open (file_path,"r",encoding = "utf-8") as file:
            return file.read()
    except Exception: 
        return ""

def extract_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    
    except Exception: 
        return ""

def extract_from_docx(file_path):
    try:
        document = Document(file_path)
        text = ""

        for para in document.paragraphs:
            if para.text.strip():
                text += para.text + "\n" 

        return text
    except Exception: 
        return ""

def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        return parse_qs(parsed_url.query).get("v",[None])[0]
    
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None 

def extract_from_youtube(youtube_url):
    video_id = get_video_id(youtube_url)

    if not video_id:
        print("YOUTUBE ERROR: Invalid video URL")
        return ""

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        text = ""

        for item in fetched_transcript:
            minutes = int(item.start // 60)
            seconds = int(item.start % 60)
            timestamp = f"{minutes:02d}:{seconds:02d}"

            text += f"[{timestamp}] {item.text}\n"

        return text

    except Exception as e:
        print("YOUTUBE ERROR:", e)
        return ""
    

def extract_from_file(file_path):
    file_path = file_path.strip()
    lower_path = file_path.lower()

    if lower_path.endswith(".txt"):
        return extract_from_txt(file_path)
    
    elif lower_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    
    if lower_path.endswith(".docx"):
        return extract_from_docx(file_path)
    else:
        return  ""


