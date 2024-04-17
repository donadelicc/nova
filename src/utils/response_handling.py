import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory


text_input_folder = os.getenv("TEXT_INPUT_FOLDER")
text_output_folder = os.getenv("TEXT_OUTPUT_FOLDER")
if not os.path.exists(text_input_folder):
    os.makedirs(text_input_folder)
if not os.path.exists(text_output_folder):
    os.makedirs(text_output_folder)

    
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1
)

conversation = ConversationChain(
    name="Nova", ## chain name
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

async def response_memory(file_name):
    
    input_file_path = os.path.join(text_input_folder, file_name)
    output_file_path = os.path.join(text_output_folder, "A.txt")
    
    with open(input_file_path, "r", encoding="utf-8") as file:
        question = file.read()

    response = conversation.predict(input=question)
    
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(response)
    return response




prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "Du er en hyggelig personlig assistent som svarer etter beste evne på spørsmål."
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation2 = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

def response_memory2(file_name):
    
    file_path = os.path.join(text_output_folder, file_name)
    
    with open(file_path, "r") as file:
        question = file.read()

    
    response = conversation2({"question": question})
    print("----------------------------")
    print("GPT-3 response:")
    text_response = response['text']
    print(text_response)
    return text_response
    

def response(file_name):

    file_path = os.path.join(text_output_folder, file_name)
    
    with open(file_path, "r") as file:
        question = file.read()

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du er en talestyrt assistent som etter beste evne prøver å besvare spørsmål som du blir stilt."},
            {"role": "user", "content": f"{question}"}
        ],
        temperature=0.1,
        max_tokens=150
        
    )
    
    output = response.choices[0].message.content
    print("----------------------------")
    print("GPT-3 response:")
    print(output)
    return output
    
