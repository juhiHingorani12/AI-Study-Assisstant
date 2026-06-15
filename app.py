import os
import markdown
from flask import Flask, render_template, request
from ai_helper import generate_response
from content_extractor import extract_from_file, extract_from_youtube

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    input_type = request.form.get("input_type")
    task_choice = request.form.get("task_choice")

    notes = ""
    source_type = "notes"

    if input_type == "paste":
        notes = request.form.get("notes", "").strip()

    elif input_type == "file":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(file_path)
            notes = extract_from_file(file_path).strip()

    elif input_type == "youtube":
        youtube_url = request.form.get("youtube_url", "").strip()
        notes = extract_from_youtube(youtube_url).strip()
        source_type = "youtube"

    if not notes:
        return render_template(
            "index.html",
            error="Could not read content. Check input, file format, or YouTube transcript availability."
        )

    result = generate_response(notes, task_choice, source_type)

    result_html = markdown.markdown(result)

    return render_template(
    "index.html",
    result=result_html,
    user_input=notes[:300]
)


if __name__ == "__main__":
    app.run(debug=True)