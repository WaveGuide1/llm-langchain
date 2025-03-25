import os
from datetime import time
from functools import lru_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

os.getenv("GROQ_API_KEY")

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

class WordClassification(BaseModel):
    sentiment: str = Field(description="Explain how the two words relates, explain in one line")
    score: int = Field(
        description="How closely is the meaning of the two words."
    )
    language: str = Field(description="The language the text is written in")


# Score words
def score_words(first_word: str, second_words: str):
    @lru_cache
    def get_llm():
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_retries=2,
        )

        structured_model = llm.with_structured_output(WordClassification)

        prompt_content = """
        Analyze the first word or text and second word or text to identify whether they have similar meaning.

        first words: {first_word}

        second words: {second_words}
        """
        prompt = ChatPromptTemplate([
            ("human", prompt_content)
        ])
        return prompt | structured_model
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def invoke_with_retry():
        try:
            llm = get_llm()
            return llm.invoke({"first_word": first_word, "second_words": second_words})
        except Exception as e:
            if "429" in str(e):
                time.sleep(2)
                raise e
            raise e

    return invoke_with_retry()


if __name__ == "__main__":
    inp1 = "Estoy muy enojado con vos! Te voy a dar tu merecido!"
    inp2 = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"
    score = score_words(inp1, inp2)
    print(score)
