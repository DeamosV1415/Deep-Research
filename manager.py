from planner import planner_agent, WebSearchItem, WebSearchPlan
from search import search_agent, SearchSnippet, SearchResult
from writer import writer_agent, FinalReport
import asyncio
from agents import Runner, trace, gen_trace_id

class ResearchManager:

  async def run(self, query: str):
    """Run the deep research process, yielding the status updates and the final report"""
    trace_id = gen_trace_id()
    with trace("Deep Research", trace_id=trace_id):
      print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
      yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
      print("Starting research...")

      search_plan = await self.plan(query)
      yield "Searches planned, starting to search..." 
      searches = await self.perform_searches(search_plan)
      yield "Searches complete, writing report..."
      report = await self.writer(searches, query)
      yield "Report Written..."
      # Streaming the report
      yield "=== Report ==="
      yield report.Report   # big markdown body

      yield "\n\n=== Conclusion ==="
      yield report.Conclusion

      yield "\n\n=== Citations ==="
      for cite in report.Citations:
          yield f"- {cite}"

  async def plan(self, query: str)-> WebSearchPlan:
    """ Plan the searches to perform for the query """
    print("Planning searches...")
    result = await Runner.run(
        planner_agent,
        f"Query: {query}",
    )
    print(f"Will perform {len(result.final_output.searches)} searches")
    return result.final_output_as(WebSearchPlan)

  async def perform_searches(self, search_plan: WebSearchPlan) -> SearchResult:
    """ Perform the searches to perform for the query """
    print("Searching...")
    num_completed = 0
    tasks = []
    for item in search_plan.searches:
        task = asyncio.create_task(self.search(item))
        await asyncio.sleep(1)   # rate-limit Brave requests
        tasks.append(task)

    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
        num_completed += 1
        print(f"Searching... {num_completed}/{len(tasks)} completed")
    print("Finished searching")
    return SearchResult(Result=results)

  async def search(self, item: WebSearchItem)-> SearchSnippet:
    """Search the web"""
    await asyncio.sleep(2)
    input = f"Search term: {item.query}\nReason for searching: {item.reason}"
    result = await Runner.run(
      search_agent,
      input  
    )
    return result.final_output_as(SearchSnippet)

  async def writer(self, result: SearchResult, query: str)-> FinalReport:
    """Writes the final report"""
    print("Thinking about report...")
    input = f"Original query: {query}\nSummarized search results: {SearchResult}"
    result = await Runner.run(
        writer_agent,
        input,
    )
    print("Finished writing report")
    return result.final_output_as(FinalReport)