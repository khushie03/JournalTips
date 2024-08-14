import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
import os

EMAIL_SERVER = "smtp.gmail.com"
PORT = 465
SENDER_EMAIL = "khushi2003p@gmail.com"
PASSWORD_EMAIL = "oora cvcr sjjd upgb"

def send_email(subject, name, receiver_email, body, journal_pdf, additional_material_pdf=None, pdf_filename="journal_tip.pdf"):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = formataddr(("AI Journal Assistant", SENDER_EMAIL))
    msg["To"] = receiver_email

    msg.attach(MIMEText(body, "plain"))

    with open(journal_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(journal_pdf))
        part['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        msg.attach(part)

    if additional_material_pdf:
        with open(additional_material_pdf, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(additional_material_pdf))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(additional_material_pdf)}"'
            msg.attach(part)

    try:
        with smtplib.SMTP_SSL(EMAIL_SERVER, PORT) as server:
            server.login(SENDER_EMAIL, PASSWORD_EMAIL)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_journal_tip(name, receiver_email, journal_tip_pdf, additional_material_pdf=None):
    subject = "Your Personalized Journal Tip"
    body = f"""
    Hi User,

    Thank you for sharing your journal entry. Based on your thoughts, we've crafted a personalized tip just for you.

    Please find the tip attached in the PDF file.

    Best regards,
    AI Journal Assistant Team
    """
    send_email(subject, name, receiver_email, body, journal_tip_pdf, additional_material_pdf, pdf_filename="journal_tip.pdf")

def summary_message(name, receiver_email, journal_tip_pdf, additional_material_pdf=None):
    subject = "Your Summarized Journal Tip"
    body = f"""
    Hi User,

    Thank you for logging into our system. Here is the summarized journal tip based on the journals you have written.

    We appreciate your involvement and look forward to seeing you again soon!

    Best regards,
    AI Journal Assistant Team
    """
    send_email(subject, name, receiver_email, body, journal_tip_pdf, additional_material_pdf, pdf_filename="summary_journal.pdf")
