from flask import Flask, render_template, request, jsonify
import sys

app = Flask(__name__)

def es_palindromo(palabra):
    """Verifica si una palabra o frase es un palíndromo."""
    palabra_limpia = ''.join(c for c in palabra if c.isalnum()).lower()
    return palabra_limpia == palabra_limpia[::-1]

def son_anagramas(palabra_principal, palabras_diccionario):
    """
    Verifica si una palabra es un anagrama de alguna palabra en una lista.
    No se incluye la palabra principal en la lista de resultados si es igual a alguna.
    """
    palabra_principal_limpia = ''.join(c for c in palabra_principal if c.isalnum()).lower()
    if not palabra_principal_limpia:
        return []
    
    principal_ordenada = sorted(palabra_principal_limpia)
    anagramas_encontrados = []
    
    for palabra in palabras_diccionario:
        palabra_limpia = ''.join(c for c in palabra if c.isalnum()).lower()
        # Se asegura de no comparar con la misma palabra y que tengan la misma longitud
        if palabra_limpia != palabra_principal_limpia and len(palabra_limpia) == len(palabra_principal_limpia):
            if sorted(palabra_limpia) == principal_ordenada:
                anagramas_encontrados.append(palabra)
                
    return anagramas_encontrados

# Un diccionario de ejemplo para verificar anagramas.
# En una aplicación real, esto se cargaría desde un archivo.
diccionario = ["amor", "roma", "mora", "ramo", "canto", "tango", "gato", "gota", "rata", "tara"]

@app.route('/')
def home():
    """Ruta principal que renderiza la página HTML."""
    return render_template('index.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    """Ruta que procesa los datos del formulario web."""
    palabra = request.form.get('palabra', '').strip()
    
    if not palabra:
        return jsonify({'resultado': "Por favor, ingresa una palabra."})

    resultado_palindromo = ""
    if es_palindromo(palabra):
        resultado_palindromo = f"'{palabra}' es un palíndromo. ¡Fantástico! 🎉"
    else:
        resultado_palindromo = f"'{palabra}' no es un palíndromo. 😔"
        
    anagramas_encontrados = son_anagramas(palabra, diccionario)
    resultado_anagramas = ""
    if anagramas_encontrados:
        lista_anagramas = ", ".join(anagramas_encontrados)
        resultado_anagramas = f"'{palabra}' tiene los siguientes anagramas en nuestra lista: {lista_anagramas}. ¡Qué interesante! ✨"
    else:
        resultado_anagramas = f"'{palabra}' no tiene anagramas conocidos en nuestra lista. 😞"
        
    resultado_final = f"{resultado_palindromo}<br>{resultado_anagramas}"
    
    return jsonify({'resultado': resultado_final})

if __name__ == '__main__':
    app.run(debug=True)