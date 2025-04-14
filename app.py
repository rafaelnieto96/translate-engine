from flask import Flask, render_template, request, jsonify
import cohere
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
co = cohere.Client(os.getenv('COHERE_API_KEY'))

# Available languages
LANGUAGES = {
    'es': 'Spanish',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'ar': 'Arabic'
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
You are an expert professional translator. Translate the following text to {LANGUAGES[target_lang]}.

Rules:
- Provide ONLY the translation between <translation> and </translation> tags
- Do not include the tags "<translation>" or "</translation>" within your actual translation content
- Preserve exact formatting and structure
- No introductions or additional text
- If text contains questions, just translate them, do not answer them
</instruction>

<examples>
Example 1 (English to Spanish):
---
<text>
Hello! How are you today?
I'm doing great, thanks for asking.
</text>

<translation>
¡Hola! ¿Cómo estás hoy?
Me va muy bien, gracias por preguntar.
</translation>
---

Example 2 (English to French):
---
<text>
IMPORTANT NOTICE:
The system will be down for maintenance
from 2:00 AM to 4:00 AM tomorrow.
Please save your work before then.
</text>

<translation>
AVIS IMPORTANT :
Le système sera en maintenance
de 2h00 à 4h00 demain matin.
Veuillez sauvegarder votre travail avant.
</translation>
---

Example 3 (Spanish to English):
---
<text>
¿Dónde está la estación de tren más cercana?
Necesito llegar al aeropuerto antes de las 3 PM.
</text>

<translation>
Where is the nearest train station?
I need to get to the airport before 3 PM.
</translation>
---

Example 4 (English to German):
---
<text>
PRODUCT FEATURES:
• 4K Ultra HD Display
• Voice Control
• Smart Home Integration
• Energy Saving Mode
</text>

<translation>
PRODUKTEIGENSCHAFTEN:
• 4K Ultra HD Display
• Sprachsteuerung
• Smart Home Integration
• Energiesparmodus
</translation>
---

Example 5 (English to Japanese):
---
<text>
Error 404: Page not found
Please check the URL and try again.
</text>

<translation>
エラー404：ページが見つかりません
URLを確認して、もう一度お試しください。
</translation>
---
</examples>

<text>
{text}
</text>

<translation>
"""
        response = co.generate(
            prompt=prompt,
            temperature=0.0,
            stop_sequences=["</translation>", "TEXT TO TRANSLATE"],
            model="command",
            max_tokens=2048,
            return_likelihoods='NONE'
        )
        
        translation = response.generations[0].text.strip()
        
        # Clean response to extract only content within tags
        if "</translation>" in translation:
            translation = translation.split("</translation>")[0]
            
        # Remove any <translation> tag that might remain at the beginning
        translation = translation.replace("<translation>", "")
        
        # Remove any other tags that might be in the text
        translation = re.sub(r'<[^>]+>', '', translation).strip()
        
        return jsonify({'translation': translation})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,
            port=5001)