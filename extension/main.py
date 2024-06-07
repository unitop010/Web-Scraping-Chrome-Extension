from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the POST request
    data = request.json
    url = data['url']
    
    # Fetch the content from the URL
    page = requests.get(url)
    
    # Use BeautifulSoup to parse and extract information
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Example: Extract all the heading tags
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    
    return jsonify({'headings': headings})

if __name__ == '__main__':
    app.run(debug=True)
