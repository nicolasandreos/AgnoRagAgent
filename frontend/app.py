import json
import uuid

import requests
import streamlit as st

AGENT_ID = "assistente-de-vale"
API_URL = f"http://localhost:7777/agents/{AGENT_ID}/runs"
SESSION_ID = "vale-session"

st.set_page_config(page_title="Assistente de Vale", page_icon="⛏️")
st.title("Assistente de Vale")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = SESSION_ID or str(uuid.uuid4())

st.caption(f"Agente `{AGENT_ID}` · sessão `{st.session_state.session_id}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def stream_agent(text: str):
    with requests.post(
        API_URL,
        data={
            "message": text,
            "session_id": st.session_state.session_id,
            "stream": "true",
        },
        stream=True,
        timeout=120,
    ) as response:
        response.raise_for_status()
        for raw in response.iter_lines():
            if not raw:
                continue
            line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
            if not line.startswith("data: "):
                continue
            try:
                event = json.loads(line[6:])
            except json.JSONDecodeError:
                continue
            if event.get("event") == "RunContent" and event.get("content"):
                yield event["content"]


if prompt := st.chat_input("Pergunte sobre a Vale..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(stream_agent(prompt))
        except requests.RequestException as exc:
            answer = f"Erro ao falar com o AgentOS: {exc}"
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer or ""})
