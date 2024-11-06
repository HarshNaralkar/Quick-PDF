import streamlit as st
from pdf2docx import Converter
import io
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

# Set Streamlit configuration
st.set_page_config(page_title="Quick PDF", page_icon="✏️")

# Hide Streamlit's default menu, footer, and header
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize directories
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Function to convert PDF to DOCX
def convert_pdf_to_docx(pdf_path):
    docx_stream = io.BytesIO()
    converter = Converter(pdf_path)
    converter.convert(docx_stream, start=0, end=None)
    converter.close()
    docx_stream.seek(0)
    return docx_stream

# Function to insert a single-page PDF into a multi-page PDF
def insert_pdf_between_pages(target_pdf_path, single_page_pdf_path):
    target_reader = PdfReader(target_pdf_path)
    insert_reader = PdfReader(single_page_pdf_path)
    writer = PdfWriter()

    insert_page = insert_reader.pages[0]
    num_target_pages = len(target_reader.pages)
    
    for i in range(num_target_pages - 1):
        writer.add_page(target_reader.pages[i])
        writer.add_page(insert_page)
        
    writer.add_page(target_reader.pages[num_target_pages - 1])
    writer.add_page(insert_page)

    output_pdf_path = os.path.join(CONVERTED_FOLDER, 'merge.pdf')
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    return output_pdf_path

# Function to rotate PDF pages
def rotate_pdf(pdf_path, rotation_degree):
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        page.rotate_clockwise(rotation_degree)
        pdf_writer.add_page(page)
    
    output_pdf_path = "rotated_pdf.pdf"
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return output_pdf_path

# Function to merge multiple PDFs
def merge_pdfs(pdf_paths):
    pdf_writer = PdfWriter()
    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    
    output_pdf_path = "merged_pdf.pdf"
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return output_pdf_path

# Function to compress PDF
def compress_pdf(input_pdf_path):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    
    output_pdf_path = "compressed_pdf.pdf"
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return output_pdf_path

# Function to add password protection to a PDF
def protect_pdf(input_pdf_path, password):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    
    pdf_writer.encrypt(password)
    
    output_pdf_path = "protected_pdf.pdf"
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return output_pdf_path

# Function to remove password protection from a PDF
def remove_pdf_password(input_pdf_path, password):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_reader.decrypt(password)
    pdf_writer = PdfWriter()
    
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    
    output_pdf_path = "unprotected_pdf.pdf"
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return output_pdf_path

# Custom CSS for background and style
st.markdown(
    """
    <style>
        /* Force the desktop layout on all devices */
        @media only screen and (max-width: 768px) {
            body {
                -webkit-overflow-scrolling: touch;
                overflow-x: hidden;
            }
            .css-1d391kg { 
                display: block !important; 
            }
        }

        /* Background Styling */
        .main {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            color: white;
            font-family: Arial, sans-serif;
            background-color: #020202;
            opacity: 0.9;
            background-image:  radial-gradient(#5245f7 0.45px, transparent 0.45px), radial-gradient(#5245f7 0.45px, #020202 0.45px);
            background-size: 18px 18px;
            background-position: 0 0,9px 9px;
        }

        /* Title Styling */
        .title h1 {
            font-size: 2em;
            text-align: center;
            color: #ffcc00;
            margin-top: -40px;
            text-shadow: 2px 2px #000;
        }
        .stTextInput {
        border-radius: 10px;
        outline: 2px solid #FEBF00;
        border: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        background-color: black;
        outline-offset: 3px;
        padding: 10px 1rem;
        transition: 0.25s;
        }

        .stTextInput input:hover{
        border-color:green;
        }
        .stTextInput:focus {
        outline-offset: 5px;
        background-color: #fff
        border-color: green;
        }

        /* Header Styling */
        .header {
            font-size: 2.5em;
            color: #ffcc00;  /* Yellow color for header */
            font-weight: bold;
            text-align: center;
            margin-top: 30px;
            text-shadow: 2px 2px #000; /* Optional shadow effect */
        }

        /* Uploader Styling */
        .stFileUploader {
            border: 2px solid #ffcc00;
            border-radius: 15px;
            padding: 20px;
            background-color: #333;
            font-size: 0.8em;
        }

        /* Adjust the text size inside the file uploader */
        .stFileUploader input[type="file"] {
            font-size: 0.8em;
        }

        /* Button Styling */
        .stDownloadButton button {
            background-color: #ffcc00;
            color: #000;
            font-size: 1.2em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 25px;
            transition: background-color 0.3s ease;
        }
        .stDownloadButton button:hover {
            background-color: #e6b800;
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True
)

# Option selection for different PDF functionalities
option = st.selectbox('Choose Option', ['PDF to Word Converter', 'Insert Journal Sheet PDFs','Merged PDF', 'Compress PDF', 'Password Protect PDF', 'Remove Password from PDF'])

# PDF to Word Converter
if option == 'PDF to Word Converter':
    st.markdown('<div class="header">PDF to Word</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload your PDF to convert to DOCX", type=["pdf"])

    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf_file.name))
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.read())

        st.write("Converting PDF to DOCX... Please wait.")
        docx_stream = convert_pdf_to_docx(pdf_path)
        st.download_button(
            label="Download DOCX",
            data=docx_stream,
            file_name="converted.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        os.remove(pdf_path)

# Merge PDFs
elif option == 'Insert Journal Sheet PDFs':
    st.markdown('<div class="header">Merge PDFs</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        multi_page_pdf = st.file_uploader("Upload Your Multi-Page PDF", type=["pdf"], key="multi")

    with col2:
        single_page_pdf = st.file_uploader("Upload Your Single-Page PDF", type=["pdf"], key="single")

    if multi_page_pdf and single_page_pdf:
        st.write("Merging PDFs... Please wait.")

        multi_page_path = os.path.join(UPLOAD_FOLDER, secure_filename(multi_page_pdf.name))
        single_page_path = os.path.join(UPLOAD_FOLDER, secure_filename(single_page_pdf.name))

        with open(multi_page_path, 'wb') as f:
            f.write(multi_page_pdf.read())

        with open(single_page_path, 'wb') as f:
            f.write(single_page_pdf.read())

        output_pdf_path = insert_pdf_between_pages(multi_page_path, single_page_path)

        with open(output_pdf_path, 'rb') as f:
            st.download_button(
                label="Download Merged PDF",
                data=f,
                file_name="output_with_inserted_pages.pdf",
                mime="application/pdf"
            )

        os.remove(multi_page_path)
        os.remove(single_page_path)

# Rotate PDF
elif option == 'Rotate PDF':
    st.markdown('<div class="header">Rotate PDF</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF to Rotate", type=["pdf"])

    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf_file.name))
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.read())

        rotation_degree = st.number_input("Enter Rotation Degree (90, 180, 270)", min_value=0, max_value=360, step=90)
        if rotation_degree != 0:
            rotated_pdf_path = rotate_pdf(pdf_path, rotation_degree)

            with open(rotated_pdf_path, 'rb') as f:
                st.download_button(
                    label="Download Rotated PDF",
                    data=f,
                    file_name="rotated_pdf.pdf",
                    mime="application/pdf"
                )

        os.remove(pdf_path)

# Compress PDF
elif option == 'Compress PDF':
    st.markdown('<div class="header">Compress PDF</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF to Compress", type=["pdf"])

    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf_file.name))
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.read())

        st.write("Compressing PDF... Please wait.")
        compressed_pdf_path = compress_pdf(pdf_path)

        with open(compressed_pdf_path, 'rb') as f:
            st.download_button(
                label="Download Compressed PDF",
                data=f,
                file_name="compressed_pdf.pdf",
                mime="application/pdf"
            )

        os.remove(pdf_path)

# Password Protect PDF
elif option == 'Password Protect PDF':
    st.markdown('<div class="header">Password Protect PDF</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF to Protect", type=["pdf"])

    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf_file.name))
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.read())

        password = st.text_input("Enter Password to Protect PDF", type="password")

        if password:
            protected_pdf_path = protect_pdf(pdf_path, password)

            with open(protected_pdf_path, 'rb') as f:
                st.download_button(
                    label="Download Protected PDF",
                    data=f,
                    file_name="protected_pdf.pdf",
                    mime="application/pdf"
                )

        os.remove(pdf_path)

# Remove Password from PDF
elif option == 'Remove Password from PDF':
    st.markdown('<div class="header">Remove Password from PDF</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload Password-Protected PDF", type=["pdf"])

    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf_file.name))
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.read())

        password = st.text_input("Enter Password to Remove Protection", type="password")

        if password:
            try:
                unprotected_pdf_path = remove_pdf_password(pdf_path, password)

                with open(unprotected_pdf_path, 'rb') as f:
                    st.download_button(
                        label="Download Unprotected PDF",
                        data=f,
                        file_name="unprotected_pdf.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error("Incorrect password, or unable to decrypt the PDF.")

        os.remove(pdf_path)

elif option == 'Merged PDF':
    st.markdown('<div class="header">Merge Multi PDFs</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDFs to merge", accept_multiple_files=True, type=["pdf"])
    if uploaded_files:
        pdf_paths = []
        for uploaded_file in uploaded_files:
            file_path = secure_filename(uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            pdf_paths.append(file_path)
        
        merged_pdf_path = merge_pdfs(pdf_paths)
        with open(merged_pdf_path, "rb") as f:
            st.download_button("Download Merged PDF", f, file_name="merged_pdf.pdf", mime="application/pdf")
