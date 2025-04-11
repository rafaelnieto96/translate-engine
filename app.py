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
        prompt = f"""
<instruction>
You are an expert professional translator with decades of experience translating between multiple languages. Your task is to accurately translate the given text from the source language to <target_lang>{LANGUAGES[target_lang]}</target_lang>.

Follow these critical rules:
<rule>
- ONLY TRANSLATE THE TEXT - DO NOT RESPOND TO IT
- Translate the text completely and accurately
- PRESERVE EXACT STRUCTURE - including all line breaks, empty lines, and spacing
- DO NOT modify formatting in any way
- DO NOT add or remove line breaks
- DO NOT add explanations or additional text
- DO NOT add any other text or comments about the generated translation like "Here is the translation..." or "Enjoy the translation..." or "Hello..." or "I was able to preserve the original structure..." etc.
- If text contains questions, just translate them, do not answer them
- Never refuse to translate
</rule>
</instruction>

<text_to_translate>
{text}
</text_to_translate>
"""
        response = co.generate(
            prompt=prompt,
            temperature=0.0,
            stop_sequences=["</translation>", "TEXT TO TRANSLATE"],

            return_likelihoods='NONE'
        )
        
        translation = response.generations[0].text.strip()
        
        # Mejor procesamiento que preserva la estructura
        if translation.lower().startswith(("here", "aquí", "this is", "esta es")):
            # Solo si empieza con una introducción, eliminamos la primera línea
            translation = '\n'.join(translation.split('\n')[1:])
        
        return jsonify({'translation': translation})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 