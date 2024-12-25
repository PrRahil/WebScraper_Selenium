from flask import Flask, request, jsonify
from scraper import WebScraper

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        scraper = WebScraper(driver_path='./chromedriver.exe')
        scraper.open_website(url)
        text_content = scraper.extract_all_text()
        scraper.close_browser()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'text_content': text_content})

if __name__ == '__main__':
    app.run(debug=True)
