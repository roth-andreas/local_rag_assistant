import streamlit as st
import os
import tempfile
from backend import ingest_pdf, query_rag

st.set_page_config(page_title="Local Knowledge Base", layout="wide")
st.title("Local RAG Assistant")
st.caption("Powered by Ollama (LLama 3) | Local and Private")

with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file is not None:
        if st.button("Ingest Document"):
            with st.spinner("Processing..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                num_chunks = ingest_pdf(tmp_path)
                os.remove(tmp_path)
                st.success(f"Ingested {num_chunks} chunks into Knowledge Base!")

st.header("2. Chat with your Data")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text, sources = query_rag(prompt)
            st.markdown(response_text)

            with st.expander("View Source Context"):
                for doc in sources:
                    st.caption(f"Page {doc.metadata.get('page', '?')}")
                    st.text(doc.page_content[:200] + "...")

    st.session_state.messages.append({"role": "assistant", "content": response_text})
