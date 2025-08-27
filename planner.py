from models import or_gpt_model
from agents import Agent
from pydantic import BaseModel, Field

Searches = 2

planner_prompt = f"""You are a helpful research assistant. Given a query, come up with a set of web searches
to perform to best answer the query. Output {Searches} terms to query for. Don't exceed the number of searches."""

class WebSearchItem(BaseModel):
  reason: str = Field(description="Your reasoning for why this search is important to the query.")
  query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
  searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

planner_agent = Agent(
  name="Planner Agent",
  model=or_gpt_model,
  instructions=planner_prompt,
  output_type=WebSearchPlan
)
