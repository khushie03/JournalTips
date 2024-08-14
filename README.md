# JournalTips
With the help of this you are able to write journals on to your personalized email also you will journal tips on to your registered mail id with that after every N hours you are able to get the summarized overview of the journal written within last N hours . This is built with the CrewAI
To provide a comprehensive README that includes both user-friendly instructions and detailed technical aspects, we'll expand the "Technical Details" section and include additional sections relevant to developers and those interested in the inner workings of the project.

```markdown
# JournalTips

Welcome to the **JournalTips** project! This web application is designed to enhance your journaling experience by providing personalized tips and summaries based on your journal entries. Whether you're a seasoned writer or just getting started, JournalTips aims to offer you insightful feedback to help guide your reflections and growth.

## Features

- **Personalized Tips**: After submitting your journal entry, receive a personalized tip crafted by our AI to help you gain new perspectives on your reflections.
- **Summary Emails**: Get thoughtful summaries of your recent journal entries, highlighting key themes and insights.
- **PDF Downloads**: Receive your tips and summaries in PDF format, making it easy to save and refer back to them later.

## How It Works

1. **Submit Your Journal**: Enter your journal entry into the system and provide your email address.
2. **Receive Your Tip**: Our AI analyzes your entry and sends you a personalized tip in PDF format via email.
3. **Request a Summary**: At any time, you can request a summary of your journal entries from the past few hours.
4. **Email Notifications**: Get all your tips and summaries conveniently sent to your email inbox.

## Getting Started

Follow these steps to start using JournalTips:

### Prerequisites

Before you begin, make sure you have the following:

- **A Web Browser**: The application runs in your web browser, so no additional software is needed.
- **Internet Connection**: Ensure you have an active internet connection to use the application and receive emails.

### Using the Application

1. **Open the Application**: Visit the [JournalTips website](https://journal.tips.com).
2. **Login**: Enter your email and password to log in.
3. **Journal Entry**: Go to the Journal page and submit your journal entry.
4. **Receive Tips**: Check your email for a PDF containing personalized tips.
5. **Summarize Entries**: Visit the Summarize page to request a summary of recent journal entries.

## Technical Details

This section provides an in-depth look at the technical aspects of JournalTips:

### Backend

- **Framework**: The application is built using [FastAPI](https://fastapi.tiangolo.com/), a modern and fast web framework for Python, known for its high performance and ease of use.
- **PDF Generation**: Utilizes [FPDF](https://pyfpdf.readthedocs.io/en/latest/) to generate PDF documents from the journal tips and summaries.
- **Email Sending**: Uses Python's `smtplib` library to securely send emails via SMTP.

### AI Agents

- **CrewAI Integration**: Leverages the CrewAI framework to create and manage AI agents that analyze journal entries and generate personalized tips and summaries.
- **Agents and Tasks**: The project defines specific agents such as the "Journal Tip Advisor" and "Reflective Summary Curator" to perform tasks like generating tips and summarizing entries.

### LLM Integration

- **Language Model**: Uses `ChatGoogleGenerativeAI` from the `langchain_google_genai` package to interact with the Gemini-1.5-Flash model for natural language processing tasks.

### Project Structure

```
├── app.py                 # Main application logic
├── agents.py              # AI agents and tasks definitions
├── send_mess.py           # Email sending functionality
├── templates/             # HTML templates for web pages
│   ├── index.html
│   ├── journal.html
│   └── summarize.html
├── static/                # Static files (e.g., CSS, JS)
└── .env                   # Environment variables file
```

### Environment Variables

The project uses environment variables to manage sensitive information such as API keys and email credentials. Ensure you have a `.env` file configured with the following:

```
GOOGLE_API_KEY=your_google_api_key_here
SENDER_EMAIL=your_email_here
PASSWORD_EMAIL=your_email_password_here
```

## Deployment

To deploy JournalTips, follow these steps:

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/khushie03/JournalTips.git
   cd JournalTips
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

4. **Access the Application**: Open your web browser and go to `http://localhost:8000`.

## Security and Privacy

Your privacy is important to us. JournalTips uses secure email protocols to ensure your data is protected. We never share your journal entries or email address with third parties.

## Troubleshooting

If you encounter any issues or have questions, please contact our support team at support@journal.tips.com.

## Contributing

We welcome contributions to enhance JournalTips! Feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.


