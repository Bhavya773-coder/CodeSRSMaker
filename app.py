import streamlit as st
import openai
from fpdf import FPDF
import streamlit.components.v1 as components
import os

# Initialize OpenAI Groq Client
client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="SRS Generator + Study Notes", layout="centered")
st.title("📄 SRS, Code Explanation & Topper Notes Generator (Groq LLaMA 3)")

uploaded_file = st.file_uploader("Upload your code file", type=["py", "txt", "js", "html", "java", "cpp", "ipynb", "md"])

# ======== AI Features ========

def generate_srs(code):
    prompt = """
    You are a software engineer creating a formal Software Requirements Specification (SRS) document for a software project.
    Your task is to create a detailed and structured SRS using the following sections:

    1. **Introduction**
    2. **Overall Description**
    3. **Specific Requirements**
    4. **External Interface Requirements**
    5. **Functional Requirements**
    6. **Non-functional Requirements**

    Ensure the language is formal and professional.
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

def generate_topper_notes(code):
    prompt = """
    You are an expert computer science tutor. Create high-quality, concise, and well-structured academic-style study notes based on the following code.

    The notes should help a student understand the logic, structure, and purpose of the code effectively. Use bullet points, simple language, and headings such as:
    
    1. **Topic Overview**
    2. **Key Concepts in the Code**
    3. **Step-by-Step Explanation**
    4. **Use Cases / Real-life Applications**
    5. **Exam Tips (if applicable)**

    These notes should feel like they're made by a top student preparing for exams or viva. Avoid jargon, and ensure clarity for easy understanding and quick revision.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate topper-style notes from this code:\n\n{code}"}
        ]
    )
    return response.choices[0].message.content

def generate_pdf(text, filename="Document.pdf"):
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

# ======== Main UI ========

if uploaded_file is not None:
    code_content = handle_uploaded_file(uploaded_file)
    st.code(code_content, language="python")
    st.markdown("---")

    # Generate SRS
    if st.button("🧠 Generate SRS Document"):
        with st.spinner("Generating SRS..."):
            srs_text = generate_srs(code_content)
            st.success("✅ SRS Document Generated")
            st.text_area("SRS Preview", srs_text, height=400)
            pdf_file = generate_pdf(srs_text, filename="SRS_Document.pdf")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download SRS PDF", f, file_name=pdf_file)

    # Generate Code Explanation
    if st.button("💡 Explain Code"):
        with st.spinner("Generating explanation..."):
            explanation = generate_code_explanation(code_content)
            st.success("✅ Code Explanation Ready")
            st.text_area("Code Explanation", explanation, height=400)

    # Generate Topper Notes
    if st.button("📚 Generate Topper Notes"):
        with st.spinner("Generating topper-style notes..."):
            notes = generate_topper_notes(code_content)
            st.success("✅ Topper Notes Generated")
            st.text_area("Topper Notes", notes, height=400)
            

            # Speak notes aloud (JS-based button)
            components.html(f"""
    <div style="margin-top: 20px;">
        <button onclick="playText()" style="padding:10px 20px;margin-right:10px;font-size:16px;">▶️ Play</button>
        <button onclick="pauseText()" style="padding:10px 20px;margin-right:10px;font-size:16px;">⏸️ Pause</button>
        <button onclick="stopText()" style="padding:10px 20px;font-size:16px;">⏹️ Stop</button>
    </div>
    <script>
        let utterance;
        let isPlaying = false;

        function playText() {{
            if (!utterance || !isPlaying) {{
                const text = `{notes.replace("`", "'").replace("\\", "\\\\").replace("\n", " ")}`;
                utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.onend = () => {{
                    isPlaying = false;
                }};
                speechSynthesis.speak(utterance);
                isPlaying = true;
            }} else if (speechSynthesis.paused) {{
                speechSynthesis.resume();
            }}
        }}

        function pauseText() {{
            if (speechSynthesis.speaking && !speechSynthesis.paused) {{
                speechSynthesis.pause();
            }}
        }}

        function stopText() {{
            if (speechSynthesis.speaking) {{
                speechSynthesis.cancel();
                isPlaying = false;
            }}
        }}
    </script>
""", height=150)


            # Download Notes PDF
            pdf_file = generate_pdf(notes, filename="Topper_Notes.pdf")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Notes PDF", f, file_name=pdf_file)

else:
    st.info("📁 Please upload a code file (e.g., Python, JS, Java, Jupyter Notebook, etc.) to begin.")
