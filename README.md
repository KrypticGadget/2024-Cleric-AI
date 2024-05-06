# Call Log Analysis

This project is a web application that processes and extracts information from a set of call logs using an LLM (Language Model). It allows users to submit questions and call log documents, extracts relevant facts using the Anthropic API, processes fact changes, and displays the extracted facts to the user.

## Features

- User-friendly Streamlit interface for submitting questions and call log documents
- FastAPI endpoints for handling question and document submission, and retrieving extracted facts
- Fact extraction using the Anthropic API to identify relevant information from call logs
- Fact change processing to track the evolution of facts over time
- Display of extracted facts for each submitted question in the output screen
- Caching of questions, facts, and fact cha
## Requirements

- Python 3.x
- Streamlit
- FastAPI
- Anthropic API Key

## Installation

1. Clone the repository:
git clone https://github.com/your-username/call-log-analysis.git
Copy code
2. Install the required dependencies:
pip install -r requirements.txt
Copy code
3. Replace the placeholder API key in `.env` with your actual Anthropic API key.

## Usage

1. Start the FastAPI server:
uvicorn api.endpoints:app --reload
Copy code
2. Start the Streamlit application:
streamlit run app.py
Copy code
3. Open the web application in your browser.

4. On the input screen, select a question from the dropdown menu and provide the URLs of the call log documents (one per line).

5. Click the "Submit" button to process the call logs and extract the relevant facts.

6. Navigate to the output screen to view the extracted facts for each submitted question.

## Project Structure

The project is organized into the following directories and files:

- `api/`: Contains the FastAPI endpoints and request/response schemas.
- `cache/`: Stores the cached JSON files for questions, facts, fact changes, and final facts.
- `data/`: Contains sample call log files for testing and demonstration purposes.
- `services/`: Implements the fact extraction and fact change processing services.
- `static/`: Contains static assets such as CSS styles.
- `utils/`: Provides utility functions for interacting with the Anthropic API and managing data.
- `app.py`: The main Streamlit application file that defines the user interface and handles user interactions.
- `file_server.py`: A Flask server for serving call log files.
- `.env`: Stores environment variables such as the Anthropic API key.
- `requirements.txt`: Lists the required Python dependencies for the project.

## Customization

- To use your own call log data, replace the sample files in the `data/` directory with your call log files.
- Modify the `static/styles.css` file to customize the appearance of the web application.
- Update the Anthropic API key in the `.env` file with your own API key.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- This project utilizes the Anthropic API for fact extraction and change processing.
- The web application is built using Streamlit and FastAPI.