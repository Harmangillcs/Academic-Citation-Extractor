import fitz  # PyMuPDF
import requests
import ast

def extract_text_chunks(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    except Exception as e:
        return [f"PDF parsing error: {str(e)}"]

def verify_with_crossref(llm_response):

    try:
        citations = ast.literal_eval(llm_response)
        if not isinstance(citations, list):
            return [{"error": "Model did not return a list."}]
    except Exception as e:
        return [{"error": f"Parsing Error: {str(e)}"}]

    verified = []
    for citation in citations:
        title = citation.get("Title")
        if not title or not isinstance(title, str):
            citation["Verified"] = False
            verified.append(citation)
            continue

        query = title.strip().replace("\n", " ")
        url = f"https://api.crossref.org/works?query.title={query}"

        try:
            response = requests.get(url, headers={"User-Agent": "CitationVerifier/1.0"})
            data = response.json()
            items = data.get("message", {}).get("items", [])
            citation["Verified"] = len(items) > 0
        except Exception as e:
            citation["Verified"] = False
            citation["error"] = str(e)

        verified.append(citation)

    return verified
