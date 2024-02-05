from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du er en talestyrt assistent som etter beste evne prøver å besvare spørsmål som du blir stilt."},
        {"role": "user", "content": "Hva er hovedstaden i Norge?"}
    ]
)

print(response.choices[0].message.content)
