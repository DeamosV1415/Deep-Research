import os
from agents import OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

#api keys
groq = os.getenv("GROQ_API_KEY")
gemini = os.getenv("GEMINI_API_KEY")
openai = os.getenv("OPENAI_API_KEY")
OR_api = os.getenv("OPENROUTER_API_KEY")
tavily_api = os.getenv("tavily_api_key")
brave_api = os.getenv("brave_search")

#base urls
groq_base_url = "https://api.groq.com/openai/v1"
gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
OR_base_url = "https://openrouter.ai/api/v1"

#clients
groq_client = AsyncOpenAI(base_url=groq_base_url, api_key=groq)
gemini_client = AsyncOpenAI(base_url=gemini_base_url, api_key=gemini)
or_client = AsyncOpenAI(base_url=OR_base_url, api_key=OR_api)

#models
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-r1-distill-llama-70b", openai_client=groq_client)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
or_gpt_model = OpenAIChatCompletionsModel(model="openai/gpt-4o-mini", openai_client=or_client)
