import streamlit as st

from rag import ask_question


st.set_page_config(
    page_title="PCB Research RAG",
    page_icon="📄",
    layout="wide"
)


st.title("📄 PCB Research RAG")
st.write("Ask questions about the uploaded PCB research knowledge base.")


question = st.text_input(
    "Enter your question",
    placeholder="Example: What is image registration in PCB inspection?"
)


if st.button("Ask", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):

            answer, sources = ask_question(question)

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Sources")

        for source in sources:
            st.write(
                f"📄 {source['source']}  |  "
                f"Page {source['page']}  |  "
                f"Chunk {source['chunk_id']}"
            )