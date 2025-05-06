import streamlit as st
import openai
from fpdf import FPDF
import os

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="SRS Generator", layout="centered")
st.title("📄 Generate SRS & Explain Code from Files (Groq LLaMA 3)")

# File uploader with multiple file types
uploaded_file = st.file_uploader("Upload your code file", type=["py", "txt", "js", "html", "java", "cpp", "ipynb", "md"])

def generate_srs(code):
    # Improved prompt for generating a more professional SRS
    prompt = """
    You are a software engineer creating a formal Software Requirements Specification (SRS) document for a software project.
    Your task is to create a detailed and structured SRS using the following sections:
    
    1. **Introduction**: Provide a high-level description of the software system, its goals, and scope.
    2. **Overall Description**: Describe the software’s functionality, users, constraints, and system dependencies.
    3. **Specific Requirements**: Outline the detailed software specifications, including performance, security, and design constraints.
    4. **External Interface Requirements**: List the external systems and interfaces the software will interact with.
    5. **Functional Requirements**: Define the core features and functionalities that the software must provide.
    6. **Non-functional Requirements**: Specify non-functional attributes such as performance, scalability, and usability.

    Ensure the language is formal and appropriate for a business setting, focusing on clarity and precision.
    """
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate an SRS document based on this code:\n\n{code}"}
        ]
    )
    return response.choices[0].message.content

def generate_code_explanation(code):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a software engineer explaining code to a beginner. Break down the code line-by-line, explaining the logic and purpose of each part."},
            {"role": "user", "content": f"Please explain the following code in simple terms:\n\n{code}"}
        ]
    )
    return response.choices[0].message.content

def generate_pdf(text, filename="SRS_Document.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

def handle_uploaded_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'ipynb':
        import nbformat
        notebook = nbformat.read(uploaded_file, as_version=4)
        code = "\n".join([cell['source'] for cell in notebook.cells if cell.cell_type == 'code'])
    else:
        code = uploaded_file.read().decode("utf-8")
    return code

if uploaded_file is not None:
    code_content = handle_uploaded_file(uploaded_file)
    
    st.code(code_content, language="python")

    st.markdown("---")
    
    # Generate SRS Button
    if st.button("🧠 Generate SRS Document"):
        with st.spinner("Generating SRS with Groq LLaMA 3..."):
            srs_text = generate_srs(code_content)
            st.success("SRS Document Generated!")
            st.text_area("SRS Preview", srs_text, height=400)
            pdf_file = generate_pdf(srs_text)
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download SRS PDF", f, file_name=pdf_file)

    # Generate Code Explanation Button
    if st.button("💡 Explain Code"):
        with st.spinner("Generating explanation..."):
            explanation_text = generate_code_explanation(code_content)
            st.success("Code Explanation Generated!")
            st.text_area("Code Explanation", explanation_text, height=400)

else:
    st.info("Please upload a code file (e.g., Python, JavaScript, Jupyter notebook, etc.) to get started.")
