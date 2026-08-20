import os
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.os import AgentOS

load_dotenv()

SCRIPTS_DIR = Path(__file__).resolve().parent
PDF_PATH = SCRIPTS_DIR / "files" / "VALE" / "base_conhecimento_vale.pdf"

db = SqliteDb(db_file=str(SCRIPTS_DIR / "tmp" / "rag-memory.db"))

vector_db = ChromaDb(
    collection="rag-collection",
    path=str(SCRIPTS_DIR / "tmp" / "chroma-db"),
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    persistent_client=True,
)

knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.add_content(
    path=str(PDF_PATH),
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Vale",
        "ticker": "VALE3",
        "sector": "Mineração",
        "country": "Brasil",
    },
    skip_if_exists=True,
)

vale_agent = Agent(
    id="assistente-de-vale",
    name="Assistente de Vale",
    model=OpenAIChat(id="gpt-5.4-mini"),
    instructions="Você é um assistente de Vale que pode ajudar o usuário a responder perguntas sobre a empresa.",
    db=db,
    debug_mode=True,
    add_history_to_context=True,
    num_history_runs=20,
    enable_user_memories=True,
    add_memories_to_context=True,
    enable_agentic_memory=True,
    add_knowledge_to_context=True,
    knowledge=knowledge,
)

agent_os = AgentOS(
    id="agent_os",
    agents=[vale_agent],
    db=db,
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://os.agno.com",
        "https://agnoragagent.onrender.com",
        "https://agnoragagent-1.onrender.com",
    ],
)

app = agent_os.get_app()

if __name__ == "__main__":
    host = os.getenv("AGENT_OS_HOST", "0.0.0.0")
    port = int(os.getenv("PORT") or os.getenv("AGENT_OS_PORT") or "7777")
    agent_os.serve(app=app, host=host, port=port, reload=False)
