from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking

load_dotenv()

db = SqliteDb(db_file="tmp/rag-memory.db")

vector_db = ChromaDb(
    collection="rag-collection",
    path="tmp/chroma-db",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    persistent_client=True    
    )

knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.add_content(
    path="files/PETR/",
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Petrobras",
        "ticker": "PETR4",
        "sector": "Petróleo e Gás",
        "country": "Brasil",
    },
    skip_if_exists=True
)

knowledge.add_content(
    path="files/VALE/",
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Vale",
        "ticker": "VALE3",
        "sector": "Mineração",
        "country": "Brasil",
    },
    skip_if_exists=True
)

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
    enable_agentic_memory=True,
    add_knowledge_to_context=True,
    knowledge=knowledge
)

# agent.print_response("A partir de agora, quero sempre que as respostas das cotações sejam em italiano e em 2 paragrafos", session_id="nicolas-session-3", user_id="nicolas")
# agent.print_response("Me chamo Pedro, prefiro receber as respostas sempre em portuguese e com textos bem longos e detalhados", session_id="pedro-session-1", user_id="pedro")

agent.print_response("Qual foi o lucro bruto da Petrobras no 2 trimestre de 2025?")
agent.print_response("Quem são Sr. Rogerio Nogueira e Sr. Shaun Usmar e qual é o cargo de cada um?")