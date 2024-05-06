import streamlit as st
import json
from api.schemas import SubmitQuestionAndDocumentsRequest
from api.endpoints import submit_question_and_documents, get_question_and_facts

def main():
    st.set_page_config(page_title="Call Log Analysis")
    st.title("Call Log Analysis")

    page = st.sidebar.radio("Select Page", ("Input", "Output"))

    if page == "Input":
        input_screen()
    else:
        output_screen()

def input_screen():
    st.header("Input")

    # Load questions from cache/question.json
    try:
        with open("cache/question.json", "r") as file:
            questions_data = json.load(file)
    except FileNotFoundError:
        questions_data = []

    # Extract questions from the loaded data
    questions = [entry["question"] for entry in questions_data]

    # Add a default option to the questions list
    questions.insert(0, "Select a question")

    # Display the dropdown with the questions
    selected_question = st.selectbox("Question", questions)

    documents = st.text_area("Call Log URLs (one URL per line)")

    if st.button("Submit"):
        if selected_question != "Select a question" and documents:
            document_urls = documents.split("\n")
            document_urls = [url.strip() for url in document_urls if url.strip()]
            request = SubmitQuestionAndDocumentsRequest(question=selected_question, documents=document_urls)
            with st.spinner("Processing..."):
                submit_question_and_documents(request)
            st.success("Processing complete. Navigate to the Output page to view the results.")
        else:
            st.warning("Please select a question and provide at least one document URL.")

def output_screen():
    st.header("Output")
    
    try:
        with open("cache/final_facts.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    questions = set(entry["question"] for entry in data)
    
    for question in questions:
        st.subheader(question)
        
        entries = [entry for entry in data if entry["question"] == question]
        
        if entries:
            latest_entry = entries[-1]
            facts = latest_entry.get("facts", [])
            
            for fact in facts:
                st.write(f"- {fact}")
        else:
            st.write("No facts available.")

if __name__ == "__main__":
    main()