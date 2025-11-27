from agents import Agent
from models import or_gpt_model
from pydantic import BaseModel, Field

class FinalReport(BaseModel):
  Conclusion: str = Field(description="A concise summary of the whole report which concludes all the findings.")
  Report: str = Field(description="The complete Markdown report with all the findings.")
  Citations: list[str] = Field(description="List of all the urls, sources and reference documents from which the Final report has been formed.")

writer_prompt = """You are a senior researcher tasked with writing a cohesive report for a research query. 
    You will be provided with the original query, and some initial research done by a research assistant.
    You should first come up with an outline for the report that describes the structure and 
    flow of the report. Then, generate the report and return that as your final output.
    The final output should be in markdown format, and it should be lengthy and detailed. Aim 
    for 5-10 pages of content, at least 1000 words. End the report with the conclusion (or summary) and the citations.""".strip()

writer_agent = Agent(
  name="Writer Agent",
  model="gpt-4o-mini",
  instructions=writer_prompt,
  output_type=FinalReport
)