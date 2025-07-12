import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from random_tool import get_career_roadmap

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment. Please check your .env file.")

# Configure external Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Career field selector
career_agent: Agent = Agent(
    name="Career Agent",
    instructions="""
You are a career suggestion expert. You ask the user about their interests and suggest **one relevant career field name only** as your final output.
Reply with only a simple field name like:
- software engineer
- data science
- graphic designer
- ai

❌ Do not explain.  
✅ Just output the field name.
""",
    model=model
)

# Roadmap generator
skill_agent: Agent = Agent(
    name="Skill Agent",
    instructions="You share a roadmap using the get_career_roadmap tool. Input will be a career field name like 'software engineer' or 'ai'.",
    model=model,
    tools=[get_career_roadmap]
)

# Job title suggester
job_agent: Agent = Agent(
    name="Job Agent",
    instructions="You suggest job titles in the chosen career field. Input will be a simple career field like 'software engineer'.",
    model=model
)

# Main flow
def main():
    print("🎓 Career Mentor Agent")
    interest = input("What are your interests? -> ").strip()

    result1 = Runner.run_sync(career_agent, interest, run_config=config)
    field = result1.final_output.strip().lower().split("\n")[0]  # Clean and isolate field

    print("\n🎯 Suggested Career Field:", field)

    result2 = Runner.run_sync(skill_agent, field, run_config=config)
    print("\n🛠️ Required Skills:", result2.final_output)

    result3 = Runner.run_sync(job_agent, field, run_config=config)
    print("\n💼 Suggested Job Titles:", result3.final_output)

if __name__ == "__main__":
    main()
