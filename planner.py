from models import or_gpt_model
from agents import Agent
from pydantic import BaseModel, Field
from datetime import datetime

Searches = 5

def get_today_str() -> str:
    """Get current date in a human-readable format."""
    try:
        return datetime.now().strftime("%a %b %#d, %Y")
    except ValueError:
        try:
            return datetime.now().strftime("%a %b %-d, %Y")
        except ValueError:
            return datetime.now().strftime("%a %b %d, %Y")

planner_prompt = f"""You are a helpful research assistant. Given a query, come up with a set of web searches
to perform to best answer the query. Output {Searches} terms to query for. Don't exceed the number of searches. 
For context, today's date is {get_today_str()} Align the searches taking today's date into consideration."""

class WebSearchItem(BaseModel):
  reason: str = Field(description="Your reasoning for why this search is important to the query.")
  query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
  searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

planner_agent = Agent(
  name="Planner Agent",
  model="gpt-4o-mini",
  instructions=planner_prompt,
  output_type=WebSearchPlan
)
