from send_mess import send_journal_tip
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import re
import firebase_admin
from firebase_admin import credentials, firestore
from fpdf import FPDF
from fastapi.responses import HTMLResponse, RedirectResponse
from agents import kickoff_journaling_process , tip_process
app = FastAPI()
from crewai import Crew,Process


cred = credentials.Certificate("C:/PROJECTS/ThoughtProcessor/thoughprocessor-bbbc3-firebase-adminsdk-9bms6-1465e75c40.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://quizapp-7bc35-default-rtdb.firebaseio.com/"})

db = firestore.client()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email and password:
        return RedirectResponse(url="/journal", status_code=303)
    else:
        return {"error": "Invalid credentials"}


from fastapi import Request

@app.get("/journal")
async def journal(request: Request):
    return templates.TemplateResponse("journal.html", {"request": request})

@app.post("/submit-journal")
async def submit_journal(request: Request, journal_entry: str = Form(...), email: str = Form(...)):
    doc_ref = db.collection("journals").document(email)
    doc_ref.set({
        "entry": journal_entry,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    journal_tip = tip_process(journal_entry)
    print("Journal Tip:", journal_tip)  # Debugging statement

    pdf_filename = f"{email}_journal_tip.pdf"
    create_pdf([journal_tip], pdf_filename)

    send_journal_tip("User", email, pdf_filename)

    return RedirectResponse(url="/", status_code=303)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
