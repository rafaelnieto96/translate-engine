from flask import Flask, render_template, request, jsonify
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
co = cohere.Client(os.getenv('COHERE_API_KEY'))

# Lista de idiomas disponibles
LANGUAGES = {
    'es': 'Español',
    'en': 'Inglés',
    'fr': 'Francés',
    'de': 'Alemán',
    'it': 'Italiano',
    'pt': 'Portugués',
    'ru': 'Ruso',
    'ja': 'Japonés',
    'zh': 'Chino',
    'ar': 'Árabe'
}

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_lang = data.get('target_lang')
    
    if not text or not target_lang:
        return jsonify({'error': 'Missing text or target language'}), 400
    
    try:
        # Usar Cohere para la traducción
        response = co.generate(
            prompt=f"Translate the following text to {LANGUAGES[target_lang]}: {text}",
            max_tokens=100,
            temperature=0.3,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        
        translation = response.generations[0].text.strip()
        return jsonify({'translation': translation})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 