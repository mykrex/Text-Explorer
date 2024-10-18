# algoritmo KMP
def kmp_search(pattern, text):
    #array LPS   
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0  
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0  
    result = []
    
    #Recorre el texto buscando el patrón
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern): #Encuentra el patrón completo
            result.append(i - j)  
            j = lps[j - 1]

        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result

#Resaltar el patrón encontrado
def highlight_text(text, pattern, indices):
    highlighted_text = ""
    last_index = 0
    for index in indices:
        highlighted_text += text[last_index:index]  
        highlighted_text += '\033[43m' + text[index:index + len(pattern)] + '\033[0m'  
        last_index = index + len(pattern)
    highlighted_text += text[last_index:]  
    return highlighted_text


# Función principal para leer el archivo y realizar la búsqueda
def main():
    file_name = input("Introduce el nombre del archivo de texto (incluyendo la extensión .txt): ")
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"El archivo '{file_name}' no fue encontrado.")
        return
    
    # Ingresar el patrón a buscar
    pattern = input("Introduce el patrón a buscar: ")

    # Buscar todas las ocurrencias del patrón
    indices = kmp_search(pattern, text)

    # Resaltar las ocurrencias encontradas
    highlighted_result = highlight_text(text, pattern, indices)

    print("\nTexto con las ocurrencias resaltadas:")
    print(highlighted_result)


# Ejecutar el programa
if __name__ == "__main__":
    main()
