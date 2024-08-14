from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta, timezone
from fpdf import FPDF
import logging
from send_mess import send_journal_tip, summary_message
from agents import kickoff_journaling_process, tip_process

app = FastAPI()

class MemoryStore:
    def __init__(self):
        self.store = {}

    def store_data(self, key, data):
        self.store[key] = data

    def recall_data(self, key):
        return self.store.get(key, None)

memory = MemoryStore()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def create_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content:
        if isinstance(line, str):
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        else:
            pdf.multi_cell(0, 10, str(line).encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln()

    pdf.output(filename)

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email and password:
        return RedirectResponse(url="/journal", status_code=303)
    else:
        return {"error": "Invalid credentials"}

@app.get("/journal")
async def journal(request: Request):
    return templates.TemplateResponse("journal.html", {"request": request})

@app.post("/submit-journal")
async def submit_journal(request: Request, journal_entry: str = Form(...), email: str = Form(...)):
    memory.store_data(email, {
        "entry": journal_entry,
        "timestamp": datetime.now(timezone.utc)
    })

    journal_tip = tip_process(journal_entry)
    logging.info(f"Journal Tip: {journal_tip}")
    pdf_filename = f"{email}_journal_tip.pdf"
    create_pdf([journal_tip], pdf_filename)

    send_journal_tip("User", email, pdf_filename)

    return RedirectResponse(url="/", status_code=303)

@app.get("/summarize", response_class=HTMLResponse)
async def summarize(request: Request):
    return templates.TemplateResponse("summarize.html", {"request": request})

@app.post("/submit-summary")
async def submit_summary(request: Request, email: str = Form(...), numberofhours: int = Form(...)):
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=numberofhours)
    logging.info(f"Time threshold: {time_threshold}")
    journal_data = memory.recall_data(email)

    if not journal_data:
        logging.info("No journal entries found for this email.")
        return {"error": "No journal entries found for this email"}

    entry_timestamp = journal_data.get('timestamp')
    logging.info(f"Timestamp from memory: {entry_timestamp}")
    recent_entries = []

    if isinstance(entry_timestamp, datetime) and entry_timestamp >= time_threshold:
        recent_entries.append(journal_data['entry'])

    if not recent_entries:
        logging.info("No recent entries found.")
        return {"error": "No journal entries found for the specified time period"}

    journal_entries_chain = "\n\n".join(recent_entries)
    summarized_result = kickoff_journaling_process(journal_entries_chain)
    pdf_filename = f"{email}_summary.pdf"
    create_pdf([summarized_result], pdf_filename)
    summary_message("User", email, pdf_filename)

    return RedirectResponse(url="/", status_code=303)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
