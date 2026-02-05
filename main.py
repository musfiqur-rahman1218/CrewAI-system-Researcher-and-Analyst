import os
import yaml
import time # Added for retry logic
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Load Environment Variables
load_dotenv()

# 2. Configure the LLM (Using Gemini 2.0 Flash)
# We use 'gemini/' because that is the official LiteLLM prefix for Google AI Studio
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash", 
    api_key=os.getenv("GEMINI_API_KEY"),
    max_retries=3,          # Bonus: Retry logic for API failures
    verbose=True
)
# 3. Manually Load YAML Configurations
with open('config/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

# 4. Initialize the Search Tool
search_tool = SerperDevTool()

# 5. Define Agents
researcher = Agent(
    config=agents_config['researcher'],
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

analyst = Agent(
    config=agents_config['analyst'],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# 6. Define Tasks
research_task = Task(
    config=tasks_config['research_task'],
    agent=researcher
)

analysis_task = Task(
    config=tasks_config['analysis_task'],
    agent=analyst
)

# 7. Assemble the Crew
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential,
    verbose=True
)

# 8. Execution with Enhanced Error Handling
if __name__ == "__main__":
    domain = input("Enter the company domain to research (e.g., shopify.com): ")
    
    try:
        print(f"\n🚀 Starting Market Research for: {domain}...\n")
        result = crew.kickoff(inputs={'company_domain': domain})
        
        print("\n\n################################################")
        print("## MARKET RESEARCH REPORT GENERATED SUCCESSFULLY ##")
        print("################################################")

    except Exception as e:
        # Check if it is a rate limit error to provide a better message
        if "429" in str(e):
            print("\n❌ Rate Limit Hit: The Free Tier quota is full.")
            print("Action: Please wait about 60 seconds and try again, or use a different Google AI Studio key.")
        else:
            print(f"\n❌ An error occurred: {e}")