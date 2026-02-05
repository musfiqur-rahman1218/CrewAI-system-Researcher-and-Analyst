# Market Research CrewAI System

This project is a multi-agent system built using [CrewAI](https://crewai.com) to perform automated market research on any given company domain. It utilizes Google's **Gemini 2.0 Flash** for analysis and **Serper** for real-time web searching.

## 🚀 Features
- **Two-Agent Architecture**: Includes a Senior Market Research Analyst and a Strategic Business Analyst.
- **YAML Configuration**: Agents and tasks are defined in separate YAML files for better maintainability.
- **Automated Output**: Generates a professional Markdown report in the `output/` directory.
- **Modern Environment**: Managed with `uv` for high-performance dependency handling.
- **Error Handling**: Implemented retry logic and try-catch blocks for robust API interactions.

## 📁 Project Structure
```text
CrewAI-system-Researcher-and-Analyst/
├── config/
│   ├── agents.yaml      # Definitions of agent roles and backstories
│   └── tasks.yaml       # Detailed task descriptions and expected outputs
├── output/              # Final generated research reports (.md)
├── .env                 # API Keys (Gemini & Serper)
├── main.py              # Main execution script
├── pyproject.toml       # Project dependencies managed by uv
└── README.md