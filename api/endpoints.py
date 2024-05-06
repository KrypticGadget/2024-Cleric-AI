import json
from fastapi import FastAPI, HTTPException
from api.schemas import SubmitQuestionAndDocumentsRequest, GetQuestionAndFactsResponse
from services.fact_extraction_service import extract_facts
from services.fact_change_service import process_fact_changes
from utils.data_management import save_question, get_question

app = FastAPI()

@app.post("/submit_question_and_documents")
def submit_question_and_documents(request: SubmitQuestionAndDocumentsRequest):
    question = request.question
    document_urls = request.documents
    
    if not question or not document_urls:
        raise HTTPException(status_code=400, detail="Question and documents are required.")
    
    save_question(question)
    print("Extracting facts...")
    extracted_facts = extract_facts(question, document_urls)
    if extracted_facts:
        print("Processing fact changes...")
        process_fact_changes(question, extracted_facts)
    else:
        print("No facts extracted. Skipping fact change processing.")
    print("Processing complete.")
    return {"message": "Question and documents submitted successfully"}

@app.get("/get_question_and_facts", response_model=GetQuestionAndFactsResponse)
def get_question_and_facts():
    try:
        with open("cache/facts.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    if data:
        latest_entry = data[-1]
        question = latest_entry["question"]
        facts = latest_entry["facts"]
        status = latest_entry["status"]
        log_processed_datetime = latest_entry.get("log_processed_datetime", "")
    else:
        question = ""
        facts = []
        status = "processing"
        log_processed_datetime = ""
    
    return GetQuestionAndFactsResponse(question=question, facts=facts, status=status, log_processed_datetime=log_processed_datetime)