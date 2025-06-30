import streamlit as st
from src.prompt import get_prompt_template
from src.model import load_model, run_chain
from src.utils import extract_text_chunks, verify_with_crossref
from src.report import generate_report
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch")
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

st.set_page_config(page_title="Academic Citation Extractor", layout="centered")
st.title("Academic Citation Extractor")

uploaded_file = st.file_uploader("Upload your academic PDF", type=["pdf"])

if uploaded_file:
    try:
        # Extract text chunks
        chunks = extract_text_chunks(uploaded_file)
        # Load the model
        llm = load_model()

        # Get prompt template
        prompt = get_prompt_template()

        # Run RAG pipeline
        result = run_chain(chunks, llm, prompt)
         #Display extracted citations
        st.subheader(" Extracted Citations")
        st.code(result["answer"], language="json")

        verified = verify_with_crossref(result["answer"])

        st.subheader("Citation Verification Results")
        st.json(verified)

        # Generate  downloading report
        report = generate_report(result["answer"], verified)
        st.download_button(" Download Report", data=report, file_name="citation_report.txt")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
