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
