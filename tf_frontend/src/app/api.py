from flask import Flask, request, jsonify
from webscraping import perform_web_scraping

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bienvenido a la API de True or Fake Job'

@app.route('/api/scrape-job', methods=['POST'])
def scrape_job():
    url = request.form.get('url')  # Obtener la URL desde los parámetros de la solicitud POST
    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    data = perform_web_scraping(url)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
