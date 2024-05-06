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