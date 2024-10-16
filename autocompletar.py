from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

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

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # No se encontraron palabras con este prefijo
            node = node.children[char]
        return self._get_words_from_node(node, prefix)

    def _get_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._get_words_from_node(child_node, prefix + char))
        return words

# Instancia del Trie global
trie = Trie()

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/cargar', methods=['POST'])
def cargar_archivo():
    if 'archivo' not in request.files:
        return "Sube un archivo."

    archivo = request.files['archivo']
    # Leer el archivo y procesar las palabras
    contenido = archivo.read().decode('utf-8')
    palabras = contenido.split()  # Se divide el texto en palabras, por espacios

    # Se insertan las palabras en el Trie
    for palabra in palabras:
        trie.insert(palabra.lower())
    
    return "Archivo cargado"

@app.route('/autocompletar', methods=['GET'])
def autocompletar():
    prefix = request.args.get('prefix', '').lower()
    suggestions = trie.search(prefix)
    return jsonify(suggestions)

if __name__ == "__main__":
    app.run(debug=True)
