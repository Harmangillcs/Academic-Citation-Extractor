from langchain.prompts import PromptTemplate

def get_prompt_template():
    return PromptTemplate(
        input_variables=["context"],
        template="""
You are a helpful assistant that extracts citation information from the following academic text.

Return a JSON array of objects containing:
- "Author"
- "Title"
- "Year"
- "Journal"
- "DOI" (null if not available)

Text:
\"\"\"{context}\"\"\"
"""
    )
