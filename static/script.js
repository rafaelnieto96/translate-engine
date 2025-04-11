document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const translateBtn = document.getElementById('translate-btn');
    const copyBtn = document.getElementById('copy-btn');
    const targetLanguage = document.getElementById('target-language');

    // Función para traducir el texto
    async function translateText() {
        const text = inputText.value.trim();
        if (!text) {
            outputText.value = 'Por favor, ingresa un texto para traducir';
            return;
        }

        try {
            translateBtn.disabled = true;
            translateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Traduciendo...';

            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    target_lang: targetLanguage.value
                })
            });

            const data = await response.json();

            if (response.ok) {
                outputText.value = data.translation;
            } else {
                outputText.value = `Error: ${data.error}`;
            }
        } catch (error) {
            outputText.value = 'Error al conectar con el servidor';
            console.error('Error:', error);
        } finally {
            translateBtn.disabled = false;
            translateBtn.innerHTML = '<i class="fas fa-exchange-alt"></i> Traducir';
        }
    }

    // Función para copiar el texto traducido
    function copyTranslation() {
        outputText.select();
        document.execCommand('copy');
        
        // Feedback visual
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    }

    // Event listeners
    translateBtn.addEventListener('click', translateText);
    copyBtn.addEventListener('click', copyTranslation);

    // Permitir traducción con Enter
    inputText.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            translateText();
        }
    });

    // Animación de entrada para los elementos
    const elements = document.querySelectorAll('.translation-box, header');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
}); 