import os

from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompts import TEMPLATE_STRING

_ = load_dotenv(find_dotenv())

api_key = os.environ.get("GOOGLE_API_KEY")

chat = ChatGoogleGenerativeAI(
    vertexai=True,
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.3,
)

parser = JsonOutputParser()
prompt_template = ChatPromptTemplate.from_template(template=TEMPLATE_STRING)

chain = prompt_template | chat | parser


async def process_message_with_ai(text: str) -> dict:
    try:
        response = await chain.ainvoke({"text": text})
        return response
    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "topic": "Error",
            "language": "Unknown",
            "sentiment": "Neutral",
            "text": "Sorry, I am having trouble processing your request right now.",
        }
