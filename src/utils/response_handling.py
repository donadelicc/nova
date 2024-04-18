import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate
)
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory


text_input_folder = os.getenv("TEXT_INPUT_FOLDER")
text_output_folder = os.getenv("TEXT_OUTPUT_FOLDER")
if not os.path.exists(text_input_folder):
    os.makedirs(text_input_folder)
if not os.path.exists(text_output_folder):
    os.makedirs(text_output_folder)


prompt= PromptTemplate(
     input_variables=['history', 'input'],
     template="""
     Du er en hyggelig og jovial AI assistent som heter Nova.
     Du svarer kort og konsist på spørsmål.
     Du dikter ikke opp ting og svarer bare dersom du vet svaret.
     Svar alltid på norsk.
     \n\nNåværende samtalehistorikk:\n{history}\n
     Human: {input}\nAI:"""
)
    
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1
)

conversation = ConversationChain(
    name="Anna", ## chain name
    llm=llm,
    verbose=True,
    prompt=prompt,
    memory=ConversationBufferMemory(),
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
