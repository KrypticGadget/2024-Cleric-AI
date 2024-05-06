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