from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tip_agent = Agent(
    role='Journal Tip Advisor',
    goal='Craft insightful and personalized tips based on user journal : {journal_entry} entries.',
    memory=True,
    backstory=(
        "You are a seasoned life coach with a deep understanding of human emotions and experiences. "
        "Your wisdom and empathy guide you in providing life-changing advice. "
        "You excel at identifying the subtle nuances in people's reflections and offering tips that resonate with their inner thoughts."
    ),
    llm=llm
)

summary_agent = Agent(
    role='Reflective Summary Curator',
    goal='Create and send thoughtful summary emails based on the last {numberofhours} hours of journal entries.',
    memory=True,
    backstory=(
        "You are a thoughtful curator of meaningful insights, with a knack for identifying recurring themes and significant moments. "
        "You carefully weave together the most important reflections, creating summaries that offer clarity and direction. "
        "Your summaries not only recap the past but also inspire and motivate for the future."
    ),
    llm=llm
)

tip_task = Task(
    description="Analyze the journal entry provided by the user and generate personalized tips that align with the entry's themes and emotions.",
    expected_output="A tip that is closely related to the content and tone of the journal entry.",
    agent=tip_agent,
    llm=llm
)

summary_task = Task(
    description="Review the journal entries from the past {numberofhours} hours and generate a summary email that highlights key themes and insights.",
    expected_output="A well-structured summary email that encapsulates the user's recent reflections.",
    agent=summary_agent,
    llm=llm
)

crew = Crew(
    agents=[tip_agent, summary_agent],
    tasks=[tip_task, summary_task],
    process=Process.sequential
)

def kickoff_journaling_process(journal_entry, summary_interval):
    inputs = {
        'journal_entry': journal_entry,
        'summary_interval': summary_interval,
    }
    result = crew.kickoff(inputs=inputs)
    print(result)


tip_crew = Crew(
    agents=[tip_agent],
    tasks=[tip_task],
    process=Process.sequential
)

def tip_process(journal_entry):
    inputs = {
        'journal_entry': journal_entry
    }
    result = tip_crew.kickoff(inputs=inputs)
    return result

tip_process("""
Journal Entry: August 13, 2024
Today felt like a day of subtle shifts—nothing too grand, but the kind of day where small things add up to something meaningful. I woke up with a sense of calm, which is a rare and welcome feeling. I took my time in the morning, allowing myself a few extra minutes to just breathe and set an intention for the day: to be present.

As I moved through the day, I found myself reflecting on the projects I'm working on. There's a lot on my plate, but instead of feeling overwhelmed, I felt a sense of purpose. Each task, no matter how small, felt like a step towards something bigger. The web applications I'm developing, the challenges I'm solving—they're all pieces of a puzzle that's slowly coming together.

I also took a moment to think about where I'm heading professionally. The internship I'm applying for at Yonder Wonder AI is on my mind. It's a step into a future I’ve been working towards, and even though there's uncertainty, there's also excitement. The possibilities in the field of computer vision are endless, and I feel ready to dive in, learn, and contribute.

In the quieter moments, I thought about balance. It's easy to get lost in work, especially when it's something I'm passionate about. But today, I made a conscious effort to step away, to enjoy a walk, to disconnect for a bit. It reminded me of the importance of pacing myself, of not losing sight of the world around me.

As the day comes to a close, I’m left with a feeling of quiet accomplishment. Not because I checked off everything on my to-do list, but because I stayed true to the intention I set this morning. I was present, and that made all the difference.

Here’s to more days like this—simple, focused, and fulfilling.
""")
