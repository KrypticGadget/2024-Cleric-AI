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