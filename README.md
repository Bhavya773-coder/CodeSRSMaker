# 📄 SRS Generator from Code (Groq LLaMA 3)

This is a simple yet powerful web application built with Streamlit that generates a **Software Requirements Specification (SRS)** document based on code files using Groq's **LLaMA 3** model. The tool supports various programming languages and formats, and it can generate an SRS document that is useful for companies and software development teams.

## Features

- **Code Upload**: Upload your code files and let the app generate an SRS document based on the code.
- **Multiple File Format Support**: Supports Python (.py), JavaScript (.js), HTML (.html), Java (.java), C++ (.cpp), and Jupyter Notebooks (.ipynb).
- **Explanation of Code**: For a deeper understanding, click **"🔍 Explain Code"** to get a detailed breakdown of the code's functionality.
- **SRS Preview**: After generating the SRS, a preview of the document will be displayed in the app.
- **Download**: You can download the generated SRS document in PDF format by clicking on the **"📥 Download SRS PDF"** button.

## Installation

To run the app locally, follow these steps:

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Step-by-Step Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Bhavya773-coder/CodeSRSMaker
   cd CodeSRSMaker
Create and activate a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
Install the required dependencies:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
Open your browser and go to http://localhost:8501 to access the app.
File Formats Supported

Python (.py)
JavaScript (.js)
HTML (.html)
Java (.java)
C++ (.cpp)
Jupyter Notebook (.ipynb)

How It Works

Upload Code: Upload your code file in one of the supported formats. The app reads the contents and processes the code.
Generate SRS: After the file is uploaded, click on "🧠 Generate SRS Document" to generate an SRS document.
View the SRS: The SRS document will be displayed in a preview window.
Download the PDF: You can download the generated SRS document by clicking on the "📥 Download SRS PDF" button.
Requirements

The application requires the following Python packages:

streamlit
openai
fpdf
These dependencies are listed in the requirements.txt file.

Contributions

Contributions are welcome! If you would like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request with your improvements.

License

This project is open-source and available under the MIT License.

Contact

If you have any questions or need support, feel free to reach out via the Issues section of this repository.

