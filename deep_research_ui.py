import gradio as gr
from dotenv import load_dotenv
from manager import ResearchManager

load_dotenv(override=True)

async def run(query: str):
    buffer = ""                  
    async for chunk in ResearchManager().run(query):
        if not isinstance(chunk, str):
            chunk = str(chunk)
        buffer += ("\n\n" + chunk) if buffer else chunk
        yield buffer 

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Researcher")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

