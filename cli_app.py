from ai_helper import generate_response
from content_extractor import extract_from_file, extract_from_youtube


print("AI STUDY ASSISSTANT")
print("=====================")
print("Choose Input Type:")
print("1.Type/paste notes")
print("2.Read from file(.pdf/.txt.docx)")
print("3.You-Tube Video Summary")
input_choice = input("Enter your Choice:")

notes = ""
source_type = notes
if input_choice == "1":
    print("\nEnter notes. Type END on a new line when finished:\n")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    notes = "\n".join(lines).strip()
    source_type = "notes"

elif input_choice=="2":
    file_path=input("Enter file path: ")
    notes= extract_from_file(file_path).strip()
    source_type = "notes"


elif input_choice=="3":
    youtube_url=input("Enter You-Tube URL : ")
    notes= extract_from_youtube(youtube_url).strip()
    source_type = "youtube"


else:
    print("Invalid choice!")
    exit()

if not notes:
    print("Could not read content")
    print("Check file path,file format , or youtube transcript availability")
    exit()

print("\nChoose task:")

if source_type == "youtube":
    print("1. Video Summary")
    print("2. Timestamp-wise Explanation")
    print("3. Generate Quiz from Video")
    print("4. Extract Video Key Points")
    print("5. Generate Viva Questions from Video")
else:
    print("1. Summarize")
    print("2. Explain")
    print("3. Generate Quiz")
    print("4. Extract Key Points")
    print("5. Generate Viva/Interview Questions")

task_choice = input("Choose:")

result = generate_response (notes,task_choice,source_type)
print("\nResult:")
print(result)

with open("output.txt","w",encoding = "utf-8") as file:
    file.write(result)

print("\nResult saved in output.txt")
