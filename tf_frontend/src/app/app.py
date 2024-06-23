from flask import Flask, render_template, request, jsonify
from webscraping import perform_web_scraping
from models import modelo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-link', methods=['POST'])
def process_link():
    url = request.form['jobLinkInput']
    data = perform_web_scraping(url)    
    prueba = modelo.predict_new_entry(data['title'], data['location'], data['company_profile'], data['description'], data['employment_type'], data['required_experience'], data['job_function'])
    return str(prueba)

if __name__ == '__main__':
    app.run(debug=True)
