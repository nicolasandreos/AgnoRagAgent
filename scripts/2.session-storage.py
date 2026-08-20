from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.tools.yfinance import YFinanceTools

load_dotenv()

db = SqliteDb(db_file="tmp/session-memory.db")

agent = Agent(
    name="Assistente de Investimentos",
    model=OpenAIChat(id="gpt-5.4-mini"),
    tools=[YFinanceTools()],
    instructions="Você é um assistente de investimentos que pode ajudar o usuário a tomar decisões de investimento.",
    db=db,
    debug_mode=True,
    add_history_to_context=True,
    num_history_runs=3
)

agent.print_response("Qual é o preço da Apple (AAPL)?", session_id="investimentos-apple")
agent.print_response("Qual é o preço da Microsoft (MSFT)?", session_id="investimentos-microsoft")
agent.print_response("Qual é o preço da Amazon (AMZN)?", session_id="investimentos-amazon")
agent.print_response("Quais cotações já foram solicitadas analises?", session_id="investimentos-apple")