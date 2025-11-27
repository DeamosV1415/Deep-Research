from dotenv import load_dotenv
from models import or_gpt_model, brave_api
from agents import Agent, function_tool, ModelSettings
from pydantic import BaseModel, Field
import requests

#TOOLS
@function_tool
def brave_search(query: str):
  "Tool for web seaches."
  url = "https://api.search.brave.com/res/v1/web/search"

  headers={
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "x-subscription-token": brave_api
  }

  params = {
      "q": query,
      "count": 10,
      "country": "us",
  }
  try:
    resp = requests.get(url=url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    responses = resp.json()

    results = responses["web"]["results"]

    data = [
        {
            "title": item.get("title"),
            "url": item.get("url"),
            "description": item.get("description"),
            "extra_snippets": item.get("extra_snippets")
        }
        for item in results
    ]
  except Exception as e:
    print(f"An error occured while searching: {e}")
    data = []

  return data

search_prompt = """You are a research assistant. Given a search term, you search the web for that term and 
    produce a concise summary of each result. The summary must 2-3 paragraphs and less than 300 
    words. Capture the main points. Write succintly, no need to have complete sentences or good 
    grammar. This will be consumed by someone synthesizing a report, so its vital you capture the 
    essence and ignore any fluff. Do not include any additional commentary other than the summary itself."""

class SearchSnippet(BaseModel):
  urls: list[str] = Field(description="List of all the urls from the search results from which information has been taken.")
  summary: str = Field(description="Summary of the search results.")

class SearchResult(BaseModel):
  Result: list[SearchSnippet] = Field(description="List of the urls and the summary of the searches.")

search_agent = Agent(
  name = "Search Agent",
  model="gpt-4o-mini",
  instructions=search_prompt,
  tools=[brave_search],
  model_settings=ModelSettings(tool_choice="required"),
  output_type=SearchSnippet
)