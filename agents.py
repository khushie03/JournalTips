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
    goal='Craft insightful and personalized tips based on user journal entry: {journal_entry}.',
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
    goal='Create and send thoughtful summary emails based on the chain of journal entries: {journal_entries}.',
    memory=True,
    backstory=(
        "You are a thoughtful curator of meaningful insights, with a knack for identifying recurring themes and significant moments. "
        "You carefully weave together the most important reflections, creating summaries that offer clarity and direction. "
        "Your summaries not only recap the past but also inspire and motivate for the future."
    ),
    llm=llm
)

tip_task = Task(
    description="Analyze the journal entry provided by the user and generate personalized tips that align with the entry's themes and emotions. Use memory to provide context-aware advice.",
    expected_output="A personalized tip closely related to the content and tone of the journal entry.",
    agent=tip_agent
)

summary_task = Task(
    description="Review the journal entries from the past N hours and generate a summary email that highlights key themes and insights.",
    expected_output="A well-structured summary email that encapsulates the user's recent reflections.",
    agent=summary_agent
)

tip_crew = Crew(
    agents=[tip_agent],
    tasks=[tip_task],
    process=Process.sequential
)

summary_crew = Crew(
    agents=[summary_agent],
    tasks=[summary_task],
    process=Process.sequential
)

def kickoff_journaling_process(journal_entries):
    inputs = {
        'journal_entries': journal_entries
    }
    print("Inputs to kickoff:", inputs)
    result = summary_crew.kickoff(inputs=inputs)
    return result

def tip_process(journal_entry):
    inputs = {
        'journal_entry': journal_entry
    }
    result = tip_crew.kickoff(inputs=inputs)
    return result
