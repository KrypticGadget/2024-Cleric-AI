from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/logs/<path:filename>')
def download_file(filename):
    return send_from_directory('C:\\Users\\krypt\\OneDrive\\Desktop\\Cleric AI\\V2\\Code\\P7\\data', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)