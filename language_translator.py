import getpass
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
import document_loader

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass(os.getenv("GROQ_API_KEY"))


model = init_chat_model("llama3-8b-8192", model_provider="groq")

system_template = "Translate the following from English into {language}"

# messages = [
#     SystemMessage("Translate the following from English into Italian"),
#     HumanMessage("How is everything from your side my friend"),
# ]

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

prompt = prompt_template.invoke({"language": "Igbo", "text": {document_loader.text_file()}})

response = model.invoke(prompt)
print(response.content)

