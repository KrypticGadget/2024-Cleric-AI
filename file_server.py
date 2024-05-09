import os
from flask import Flask, send_from_directory

app = Flask(__name__)

# Use an environment variable to define the path, or default to a relative path
DATA_DIR = os.getenv('DATA_DIRECTORY', 'data')

@app.route('/logs/<path:filename>')
def download_file(filename):
    return send_from_directory(DATA_DIR, filename)

if __name__ == '__main__':
    # Bind to PORT if defined, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
