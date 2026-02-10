import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Load Environment Variables
load_dotenv()

# 2. Configure the LLM via OpenRouter
# We use OpenRouter as the provider to avoid direct Gemini API quota issues.
# OpenRouter is OpenAI-compatible, so we set the base_url accordingly.
openrouter_llm = LLM(
    model="openrouter/google/gemini-2.0-flash-001",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_retries=3,          # Bonus: Implements retry logic for API failures
    verbose=True
)

# 3. Manually Load YAML Configurations
with open('config/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

# 4. Initialize the Search Tool
search_tool = SerperDevTool()

# 5. Define Agents using YAML config
researcher = Agent(
    config=agents_config['researcher'],
    tools=[search_tool],
    llm=openrouter_llm,
    verbose=True,
    allow_delegation=False
)

analyst = Agent(
    config=agents_config['analyst'],
    llm=openrouter_llm,
    verbose=True,
    allow_delegation=False
)

# 6. Define Tasks using YAML config
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

# 8. Execution with Error Handling
if __name__ == "__main__":
    domain = input("Enter the company domain to research (e.g., shopify.com): ")
    
    try:
        print(f"\n🚀 Starting Market Research for: {domain}...\n")
        result = crew.kickoff(inputs={'company_domain': domain})
        
        print("\n\n################################################")
        print("## MARKET RESEARCH REPORT GENERATED SUCCESSFULLY ##")
        print("################################################")
        print("Final report saved to: output/report.md")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")