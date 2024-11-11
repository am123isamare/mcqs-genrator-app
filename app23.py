import streamlit as st
import PyPDF2
import docx2txt
import random 
import re

# Function to extract text from different file types
def extract_text_from_file(file):
    text = ""
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(file)
    
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    
    else:
        st.error("Unsupported file format. Please upload a PDF, Word, or text file.")
    
    return text

# Improved MCQ Generation Function
def generate_mcqs(text, num_questions):
    sentences = re.split(r'[.!?]', text)  # Split by sentences based on punctuation
    mcqs = []
    
    for i, sentence in enumerate(sentences[:num_questions]):
        # Skip empty sentences
        if not sentence.strip():
            continue

        # Create a question based on the content
        question = f"What is the main idea of this sentence: '{sentence.strip()}'?"
        
        # Extract key terms for options (example logic: keywords in sentence)
        words = [word for word in sentence.split() if len(word) > 3]
        if len(words) >= 4:
            answer = random.choice(words)
            options = [answer] + random.sample(words, 3)
        else:
            answer = "The main idea"
            options = [answer, "Option 1", "Option 2", "Option 3"]

        random.shuffle(options)  # Shuffle options for variety
        
        mcq = {
            "question": question,
            "answer": answer,
            "options": options
        }
        mcqs.append(mcq)
    
    return mcqs

# Streamlit UI
st.title("Enhanced MCQ Generator from Document")
st.write("Upload a document (PDF, Word, or Text), and this app will generate more relevant MCQs for you.")

# File Upload
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

# Number of questions input
num_questions = st.number_input("Enter the number of MCQs you want to generate", min_value=1, max_value=20, step=1)

if uploaded_file is not None:
    # Extract text from the uploaded file
    text = extract_text_from_file(uploaded_file)
    
    # Generate MCQs if text extraction was successful
    if text:
        mcqs = generate_mcqs(text, num_questions)
        
        # Display MCQs
        st.write("### Generated MCQs:")
        for i, mcq in enumerate(mcqs, 1):
            st.write(f"**Q{i}. {mcq['question']}**")
            for option in mcq['options']:
                st.write(f"- {option}")
            st.write(f"**Answer:** {mcq['answer']}")
            st.write("---")
