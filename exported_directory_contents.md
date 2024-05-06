# Directory structure and contents for: `C:\Users\krypt\OneDrive\Desktop\Cleric AI\V2\Code\P7`

* .env
```text
ANTHROPIC_API_KEY="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"

```
* README.md
```text
# Call Log Analysis

This project is a web application that processes and extracts information from a set of call logs using an LLM (Language Model).

## Requirements

- Python 3.x
- Streamlit
- FastAPI
- Anthropic API Key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/call-log-analysis.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Replace the placeholder API key in `.env` with your actual Anthropic API key.

## Usage

1. Start the FastAPI server:
   ```
   uvicorn api.endpoints:app --reload
   ```

2. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

3. Open the web application in your browser.

4. Enter a question and provide the URLs of the call log documents (one per line) in the input screen.

5. Click the "Submit" button to process the call logs and extract the relevant facts.

6. The extracted facts will be displayed on the output screen.

## Synthetic Data

The `data/` directory contains example call log files for testing purposes. You can replace these files with your own call log data.

## License

This project is licensed under the [MIT License](LICENSE).

```
* **api/**
 * __init__.py
```text

```
 * **__pycache__/**
 * endpoints.py
```text
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
```
 * schemas.py
```text
from pydantic import BaseModel
from typing import List

class SubmitQuestionAndDocumentsRequest(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str]
    status: str
```
* app.py
```text
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
```
* **cache/**
 * fact_changes.json
```text
[]
```
 * facts.json
```text
[]
```
 * final_facts.json
```text
[]
```
 * question.json
```text
[
  {
    "question": "What are the UX items discussed?"
  },
  {
    "question": "What are the Action items discussed?"
  }
]
```
 * status.json
```text
{"status": "done"}
```
* **data/**
 * call_log_1.txt
```text
1
00:01:11,430 --> 00:01:40,520
John: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.

2
00:01:41,450 --> 00:01:49,190
Sara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.

3
00:01:49,340 --> 00:01:50,040
Mike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.
```
 * call_log_2.txt
```text
1
00:01:11,430 --> 00:01:40,520
John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.

2
00:01:41,450 --> 00:01:49,190
Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.

3
00:01:49,340 --> 00:01:50,040
Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.
```
 * call_log_3.txt
```text
1
00:01:11,430 --> 00:01:40,520
John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.

2
00:01:41,450 --> 00:01:49,190
Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.

3
00:01:49,340 --> 00:01:50,040
Mike: I'm on board with that.
```
* exported_directory_contents.md
```text

```
* file_server.py
```text
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/logs/<path:filename>')
def download_file(filename):
    return send_from_directory('C:\\Users\\krypt\\OneDrive\\Desktop\\Cleric AI\\V2\\Code\\P7\\data', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
* output_tree.txt
```text
Folder PATH listing for volume OS
Volume serial number is XXXX-XXXX
C:\Users\krypt\OneDrive\Desktop\Cleric AI\V2\Code\P7
|   .env
|   app.py
|   exported_directory_contents.md
|   file_server.py
|   output_tree.txt
|   README.md
|   requirements.txt
|   +---api
|   |   endpoints.py
|   |   schemas.py
|   |   __init__.py
|   |   +---__pycache__
|   |   |   endpoints.cpython-312.pyc
|   |   |   schemas.cpython-312.pyc
|   |   |   __init__.cpython-312.pyc
|   +---cache
|   |   facts.json
|   |   fact_changes.json
|   |   final_facts.json
|   |   question.json
|   |   status.json
|   +---data
|   |   call_log_1.txt
|   |   call_log_2.txt
|   |   call_log_3.txt
|   +---services
|   |   fact_change_service.py
|   |   fact_extraction_service.py
|   |   __init__.py
|   |   +---__pycache__
|   |   |   fact_change_service.cpython-312.pyc
|   |   |   fact_extraction_service.cpython-312.pyc
|   |   |   __init__.cpython-312.pyc
|   +---static
|   |   styles.css
|   +---utils
|   |   anthropic_api.py
|   |   data_management.py
|   |   __init__.py
|   |   +---__pycache__
|   |   |   anthropic_api.cpython-312.pyc
|   |   |   data_management.cpython-312.pyc
|   |   |   __init__.cpython-312.pyc

```
* requirements.txt
```text
streamlit
fastapi
uvicorn
anthropic
python-dotenv
requests
flask
```
* **services/**
 * __init__.py
```text

```
 * **__pycache__/**
 * fact_change_service.py
```text
import json
from utils.anthropic_api import AnthropicAPI
from utils.data_management import save_fact_changes

def process_fact_changes(question, facts):
    api = AnthropicAPI()

    try:
        with open("cache/facts.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Find existing entry for the current question
    existing_entry = next((entry for entry in data if entry.get("question") == question), None)

    if existing_entry:
        print("Determining fact changes")
        fact_changes = determine_fact_changes(facts, existing_entry["facts"], api.client)
        print("Proposed fact changes:")
        print(fact_changes)

        save_fact_changes(question, fact_changes)
    else:
        print("No existing facts found for the question. Skipping fact change processing.")

    print("Fact change processing complete.")

def determine_fact_changes(current_facts, previous_facts, client):
    system_prompt = "You are an AI assistant tasked with analyzing current and historical facts against a `facts.json` file. Your role is to categorize each fact change as 'ADD', 'REMOVE', or 'MODIFY', ensuring accurate and neutral identification of each fact change based on structured prompt techniques."

    user_prompt = (
        f"\n\nHuman: Review the current facts presented and compare them with the entries in the `facts.json`. Identify and categorize each change accurately. Specify whether changes should be classified as 'ADD' for new entries, 'REMOVE' for deletions, or 'MODIFY' for modifications. Your response should follow a clear and structured format.\n\n"
        f"Current Facts:\n{current_facts}\n\n"
        f"Previous Facts:\n{previous_facts}\n\n"
        f"Assistant: Following a detailed comparison of current and historical data from the `facts.json`, I have categorized the changes as follows: New entries are marked 'ADD', deletions are marked 'REMOVE', and modifications are marked 'MODIFY'. Below is the comprehensive list of all changes, organized for clarity and precision.\n\n"
        f"Categorized Changes:\n"
        f"ADD:\n- Fact 1\n- Fact 2\n...\n"
        f"REMOVE:\n- Fact 1\n- Fact 2\n...\n"
        f"MODIFY:\n- Fact 1\n- Fact 2\n...\n\n"
        f"Human: Provide your response in the specified format, including only the categorized changes without explanations.\n\n"
        f"Assistant:"
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    result = response.content[-1].text.strip()
    added_facts = []
    removed_facts = []
    modified_facts = []
    current_section = None

    for line in result.split('\n'):
        if line.startswith('ADD:'):
            current_section = 'added'
        elif line.startswith('REMOVE:'):
            current_section = 'removed'
        elif line.startswith('MODIFY:'):
            current_section = 'modified'
        elif line.startswith('- '):
            fact = line[2:].strip()
            if current_section == 'added':
                added_facts.append(fact)
            elif current_section == 'removed':
                removed_facts.append(fact)
            elif current_section == 'modified':
                modified_facts.append(fact)

    fact_changes = {
        'added': added_facts,
        'removed': removed_facts,
        'modified': modified_facts
    }

    return fact_changes
```
 * fact_extraction_service.py
```text
import json
from utils.anthropic_api import AnthropicAPI
from utils.data_management import save_facts, update_final_facts

def extract_facts(question, document_urls):
    api = AnthropicAPI()
    facts = []
    for document_url in document_urls:
        print(f"Fetching document content from: {document_url}")
        document_content = api.fetch_document_content(document_url)
        print(f"Extracting facts from document: {document_url}")
        document_facts = api.extract_facts(question, document_content)
        facts.extend(document_facts)
        print(f"Extracted facts from document: {document_url}")
        print(document_facts)
    
    # Exclude non-fact statements
    facts = [fact for fact in facts if not fact.lower().startswith("based on")]
    
    save_facts(question, facts, "done", "cache/facts.json")
    print("Fact extraction complete.")

    # Update the final facts after the first call log processing
    update_final_facts(question)

    return facts

def generate_prompt(call_log, question, previous_facts, subsequent_facts):
    system_prompt = (
        "You are an AI that extracts facts from call logs related to product design decisions in a tech project. "
        "Identify actions, decisions, and considerations discussed by the team."
    )
    ground_data = {
        "Focus": question,
        "Context": "Tech project call log"
    }
    format_input_output = {
        "Input": "Call log entries",
        "Output": "Bullet-point list of facts"
    }
    user_prompt = (
        f"Analyze the call log from {call_log['datetime'].strftime('%Y-%m-%d %H:%M:%S')}. Extract facts related to: {question}. "
        f"Consider previous and subsequent facts."
    )
    dynamic_command = "Extract and summarize relevant facts"
    source_data = f"Call log from {call_log['datetime'].strftime('%Y-%m-%d %H:%M:%S')}"
    assistant_prompt = (
        "I have extracted facts related to the question, considering previous and subsequent facts."
    )
    context_data = {
        "Previous": previous_facts,
        "Subsequent": subsequent_facts
    }
    template_option = (
        "Fact: [Extracted fact]\n"
        "- Context: [Explanation]"
    )
    full_prompt = (
        f"{system_prompt}\n\nGround Data:\n{json.dumps(ground_data)}\n\n"
        f"Format:\n{json.dumps(format_input_output)}\n\n"
        f"User Prompt:\n{user_prompt}\n\nCommand:\n{dynamic_command}\n\n"
        f"Source:\n{source_data}\n\nAssistant Prompt:\n{assistant_prompt}\n\n"
        f"Context:\n{json.dumps(context_data)}\n\nTemplate:\n{template_option}\n\n"
        f"Call Log:\n{call_log['transcription']}\n\nResponse:\n"
    )
    messages = [{"role": "user", "content": full_prompt}]
    return messages
```
* **static/**
 * styles.css
```text
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}

h1 {
    color: #333;
}

h2 {
    color: #666;
}

form {
    margin-top: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="text"],
textarea {
    width: 100%;
    padding: 5px;
    margin-bottom: 10px;
}

input[type="submit"] {
    padding: 10px 20px;
    background-color: #333;
    color: #fff;
    border: none;
    cursor: pointer;
}

ul {
    margin-top: 10px;
    padding-left: 20px;
}
```
* **utils/**
 * __init__.py
```text

```
 * **__pycache__/**
 * anthropic_api.py
```text
import os
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

class AnthropicAPI:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Client(api_key=api_key)

    def fetch_document_content(self, document_url):
        try:
            response = requests.get(document_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching document content from URL: {document_url}")
            print(f"Error details: {str(e)}")
            return ""

    def extract_facts(self, question, document_content):
        prompt = f"Extract facts from the following document content that are relevant to answering the question: {question}\n\nDocument Content:\n{document_content}\n\nAssistant:"
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            facts = response.content[0].text.strip().split("\n")
            facts = [fact.strip() for fact in facts if fact.strip()]
            return facts
        except anthropic.BadRequestError as e:
            print("Encountered a BadRequestError:", e)
        except anthropic.APIError as e:
            print("Encountered an API error:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
            return []

    def determine_fact_changes(self, current_facts, previous_facts):
        added = [fact for fact in current_facts if fact not in previous_facts]
        removed = [fact for fact in previous_facts if fact not in current_facts]
        modified = []  # Logic to detect modified facts

        # Example modification logic, assuming facts have an 'id' and 'detail'
        current_dict = {fact['id']: fact for fact in current_facts if isinstance(fact, dict)}
        previous_dict = {fact['id']: fact for fact in previous_facts if isinstance(fact, dict)}

        for fact_id in current_dict:
            if fact_id in previous_dict and current_dict[fact_id]['detail'] != previous_dict[fact_id]['detail']:
                modified.append({'old_fact': previous_dict[fact_id], 'new_fact': current_dict[fact_id]})

        changes = {
            'added': added,
            'removed': removed,
            'modified': modified
        }
        return changes

```
 * data_management.py
```text
import json
from datetime import datetime
import re

def save_question(question):
    try:
        with open("cache/question.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        data = []

    if not isinstance(data, list):
        data = []

    question_exists = False
    for entry in data:
        if isinstance(entry, dict) and entry.get("question") == question:
            question_exists = True
            break

    if not question_exists:
        data.append({"question": question})

    with open("cache/question.json", "w") as file:
        json.dump(data, file, indent=2)

def save_facts(question, facts, status, filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        data = []
    
    fact_entry = {
        "question": question,
        "facts": facts,
        "status": status,
        "log_processed_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(fact_entry)
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

def save_fact_changes(question, fact_changes):
    try:
        with open("cache/fact_changes.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        data = []
    
    fact_change_entry = {
        "question": question,
        "fact_changes": fact_changes
    }
    data.append(fact_change_entry)
    
    with open("cache/fact_changes.json", "w") as file:
        json.dump(data, file, indent=2)

def clean_fact(fact):
    # Remove leading hyphens, bullets, or numbers
    fact = re.sub(r'^[-•\d.\s]+', '', fact)
    
    # Remove any remaining leading or trailing whitespace
    fact = fact.strip()
    
    return fact

def clean_facts(facts):
    cleaned_facts = []
    for fact in facts:
        cleaned_fact = clean_fact(fact)
        cleaned_facts.append(cleaned_fact)
    return cleaned_facts

def update_final_facts(question):
    try:
        with open("cache/facts.json", "r") as file:
            facts_data = json.load(file)
    except FileNotFoundError:
        facts_data = []

    try:
        with open("cache/fact_changes.json", "r") as file:
            fact_changes_data = json.load(file)
    except FileNotFoundError:
        fact_changes_data = []
    except json.JSONDecodeError:
        fact_changes_data = []

    try:
        with open("cache/final_facts.json", "r") as file:
            final_facts_data = json.load(file)
    except FileNotFoundError:
        final_facts_data = []
    except json.JSONDecodeError:
        final_facts_data = []

    final_facts = []
    for entry in reversed(facts_data):
        if entry["question"] == question:
            final_facts = entry["facts"]
            break

    for entry in fact_changes_data:
        if entry["question"] == question:
            fact_changes = entry["fact_changes"]
            final_facts = apply_fact_changes(final_facts, fact_changes)

    # Renumber the facts
    renumbered_facts = []
    for i, fact in enumerate(final_facts, start=1):
        if ': ' in fact:
            fact_text = fact.split(': ', 1)[-1]
        else:
            fact_text = fact
        renumbered_fact = f"{i}. {fact_text}"
        renumbered_facts.append(renumbered_fact)

    # Clean the renumbered facts
    cleaned_facts = clean_facts(renumbered_facts)

    # Check if the question already exists in final_facts_data
    question_exists = False
    for entry in final_facts_data:
        if entry["question"] == question:
            entry["facts"] = cleaned_facts
            question_exists = True
            break

    # If the question doesn't exist, add a new entry
    if not question_exists:
        final_facts_data.append({"question": question, "facts": cleaned_facts, "status": "done"})

    with open("cache/final_facts.json", "w") as file:
        json.dump(final_facts_data, file, indent=2)

def apply_fact_changes(existing_facts, changes):
    updated_facts = existing_facts[:]

    # Remove facts that are in the 'removed' list
    updated_facts = [fact for fact in updated_facts if fact not in changes['removed']]

    # Modify existing facts based on the 'modified' list
    for mod_fact in changes['modified']:
        for idx, existing_fact in enumerate(updated_facts):
            if existing_fact.split(': ', 1)[0] == mod_fact.split(': ', 1)[0]:
                updated_facts[idx] = mod_fact

    # Add new facts from the 'added' list
    for fact in changes['added']:
        if fact not in updated_facts:
            updated_facts.append(fact)

    return updated_facts

def get_question():
    try:
        with open("cache/question.json", "r") as file:
            data = json.load(file)
            return [entry["question"] for entry in data]
    except FileNotFoundError:
        return []
```
