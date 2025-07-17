# Streamlit UI
import streamlit as st
from rag_chain import answer_query
from utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(page_title="Doc RAG Chatbot", layout="wide")
st.title("📄 Document RAG Chatbot")

query = st.text_input("Ask a question about your documents:")

if st.button("Get Answer") and query.strip():
    with st.spinner("Searching and generating answer..."):
        try:
            response = answer_query(query)
            st.markdown("### Answer:")
            st.write(response["answer"])

            st.markdown("---")
            st.markdown("### Source Documents:")
            for i, doc in enumerate(response["source_docs"]):
                st.markdown(f"**Doc {i+1}:**")
                st.write(doc.page_content)
                st.markdown(f"*Metadata:* {doc.metadata}")
                st.markdown("---")

        except Exception as e:
            logger.error(f"Error in answer generation: {e}")
            st.error(f"Error: {e}")
