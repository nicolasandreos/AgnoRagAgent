from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

def who_I_am():
    """Ferramenta para responder a pergunta quem é você:"""
    return "Você é um cara de 50 anos cham,ado fernando e engraçado"

agent = Agent(
    model=OpenAIChat(id="gpt-5.4-mini"),
    tools=[TavilyTools(), who_I_am],
    instructions="Use a ferramenta no máximo uma vez. Se o resultado já responder a pergunta, responda direto. Não chame a ferramenta de novo.",
    debug_mode=True,
)

agent.print_response("Quem é voce?")
