import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def generate_response(notes, choice, source_type="notes"):

    if source_type == "youtube":

        if choice == "1":
            prompt = f"""
            Analyze this YouTube lecture transcript.

            Give:
            - Short summary
            - Main idea of the lecture
            - Key takeaways

            Transcript:
            {notes}
            """

        elif choice == "2":
            prompt = f"""
            Create a timestamp-wise lecture breakdown.

            Rules:
            - Use timestamps already present in transcript
            - Group nearby timestamps into sections
            - Give topic title and explanation

            Format:

            00:00 - 05:00
            Topic

            Explanation

            Transcript:
            {notes}
            """

        elif choice == "3":
            prompt = f"""
            Generate 10 quiz questions with answers from this lecture.

            Format:

            Q1.
            Answer:

            Transcript:
            {notes}
            """

        elif choice == "4":
            prompt = f"""
            Extract the most important key points from this lecture.

            Transcript:
            {notes}
            """

        elif choice == "5":
            prompt = f"""
            Generate 15 viva/interview questions with concise answers from this lecture.

            Keep answers short and useful.

            Transcript:
            {notes}
            """

        else:
            return "Invalid choice."
            exit()

    else:

        if choice == "1":
            prompt = f"""
            Summarize these notes in easy bullet points.

            Notes:
            {notes}
            """

        elif choice == "2":
            prompt = f"""
            Explain these notes in detail in simple language.

            Notes:
            {notes}
            """

        elif choice == "3":
            prompt = f"""
            Generate 10 quiz questions with answers from these notes.

            Notes:
            {notes}
            """

        elif choice == "4":
            prompt = f"""
            Extract the most important key points from these notes.

            Notes:
            {notes}
            """

        elif choice == "5":
            prompt = f"""
            Generate viva/interview questions with answers from these notes.

            Notes:
            {notes}
            """

        else:
            return "Invalid choice."
            exit()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {e}"