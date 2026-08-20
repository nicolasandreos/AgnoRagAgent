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
    num_history_runs=3,
    enable_user_memories=True,
    add_memories_to_context=True,
    enable_agentic_memory=True
)

# agent.print_response("A partir de agora, quero sempre que as respostas das cotações sejam em italiano e em 2 paragrafos", session_id="nicolas-session-3", user_id="nicolas")
# agent.print_response("Me chamo Pedro, prefiro receber as respostas sempre em portuguese e com textos bem longos e detalhados", session_id="pedro-session-1", user_id="pedro")

agent.print_response("Qual é o preço da Apple (AAPL)?", session_id="nicolas-session-2", user_id="nicolas")
# agent.print_response("Qual é o preço da Microsoft (MSFT)?", session_id="pedro-session-2", user_id="pedro")