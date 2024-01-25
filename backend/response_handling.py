import os
from openai import OpenAI


text_outut_folder = "text_files"
if not os.path.exists(text_outut_folder):
    os.makedirs(text_outut_folder)

def response(file_name):
    
    file_path = os.path.join(text_outut_folder, file_name)
    
    with open(file_path, "r") as file:
        question = file.read()

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du er en talestyrt assistent som etter beste evne prøver å besvare spørsmål som du blir stilt."},
            {"role": "user", "content": f"{question}"}
        ]
    )
    output = response.choices[0].message.content
    print("----------------------------")
    print("GPT-3 response:")
    print(output)
    return output