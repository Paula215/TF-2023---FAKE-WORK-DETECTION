from flask import Flask, render_template, request, jsonify
from webscraping import perform_web_scraping

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-link', methods=['POST'])
def process_link():
    url = request.form['jobLinkInput']
    data = perform_web_scraping(url)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
