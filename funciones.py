from flask import Flask, render_template, request, jsonify, send_from_directory
import re
import os

app = Flask(__name__, template_folder='templates', static_folder='templates')

# FUNCION LCS (SIMILITUD)
def lcs(T1, T2):
    n, m = len(T1), len(T2)
    dp = [[0] * (m+1) for _ in range(n+1)]
    max_len, end_idx = 0, 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            if T1[i-1] == T2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_idx = i
            else:
                dp[i][j] = 0

    return T1[end_idx - max_len:end_idx]

# FUNCION TRIE (AUTO - COMPLETAR)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return sorted(self._get_words_from_node(node, prefix), key=lambda x: x[1], reverse=True)

    def _get_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append((prefix, node.frequency))
        for char, child_node in node.children.items():
            words.extend(self._get_words_from_node(child_node, prefix + char))
        return words

# Instancia del Trie
trie = Trie()


# FUNCION MANACHER (Palindromo)
def manacher(text):
    T = '#' + '#'.join(text) + '#'
    n = len(T)
    P = [0] * n
    C = R = 0
    for i in range(1, n-1):
        if i < R:
            P[i] = min(R - i, P[2*C - i])
        while i + P[i] + 1 < n and i - P[i] - 1 >= 0 and T[i + P[i] + 1] == T[i - P[i] - 1]:
            P[i] += 1
        if i + P[i] > R:
            C, R = i, i + P[i]
    
    max_len = max(P)
    center = P.index(max_len)
    start = (center - max_len) // 2
    
    return text[start:start+max_len]

# Se manda al index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('templates', path)

@app.route('/similitud', methods=['POST'])
def similitud():
    if 'archivo1' not in request.files or 'archivo2' not in request.files:
        return jsonify({"error": "Por favor sube ambos archivos."})
    
    archivo1 = request.files['archivo1']
    archivo2 = request.files['archivo2']
    
    T1 = archivo1.read().decode('utf-8')
    T2 = archivo2.read().decode('utf-8')
    
    resultado_lcs = lcs(T1, T2)
    
    return jsonify({
        "subcadena_comun": resultado_lcs
    })

@app.route('/cargar', methods=['POST'])
def cargar_archivo():
    if 'archivo' not in request.files:
        return jsonify({"error": "Sube un archivo."})

    archivo = request.files['archivo']
    contenido = archivo.read().decode('utf-8')
    palabras = re.findall(r'\b\w+\b', contenido.lower())

    for palabra in palabras:
        trie.insert(palabra)

    return jsonify({"message": "Archivo cargado correctamente.", "palabras_cargadas": len(palabras)})

@app.route('/autocompletar', methods=['GET'])
def autocompletar():
    prefix = request.args.get('prefix', '').lower()
    suggestions = trie.search(prefix)
    return jsonify([{"word": word, "frequency": freq} for word, freq in suggestions[:10]])

@app.route('/manacher', methods=['POST'])
def palindromo_manacher():
    if 'archivo' not in request.files:
        return jsonify({"error": "Por favor sube un archivo."})
    
    archivo = request.files['archivo']
    contenido = archivo.read().decode('utf-8').lower()
    
    palindromo = manacher(contenido)
    
    return jsonify({
        "palindromo": palindromo,
        "longitud": len(palindromo),
        "posiciones": [m.start() for m in re.finditer(re.escape(palindromo), contenido)]
    })

if __name__ == "__main__":
    app.run(debug=True)