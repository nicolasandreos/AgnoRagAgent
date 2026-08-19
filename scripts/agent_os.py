from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv

load_dotenv()


researcher = Agent(
    id="agent_researcher",
    name="Researcher",
    model=OpenAIChat(id="gpt-5.4-mini"),
    tools=[TavilyTools()],
)

agent_os = AgentOS(
    id="agent_os",
    agents=[researcher],
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://os.agno.com",
    ],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agent_os:app", port=7777, reload=True)