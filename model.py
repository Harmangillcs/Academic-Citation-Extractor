from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import streamlit as st

@st.cache_resource
def load_model():
    model_name = "meta-llama/Llama-2-7b-chat-hf"  # or change model acc to your choice

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    return HuggingFacePipeline(pipeline=pipe)

def run_chain(chunks, llm, prompt):
    docs = [Document(page_content=chunk.strip()) for chunk in chunks if chunk.strip()]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    doc_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    rag = create_retrieval_chain(retriever=retriever, combine_docs_chain=doc_chain)


    return rag.invoke({"input": docs[0].page_content if docs else ""})