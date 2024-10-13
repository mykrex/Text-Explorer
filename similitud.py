def lcs(T1, T2):
    n = len(T1)
    m = len(T2)

    # Crear matriz de tamano (n+1)x(m+1)
    dp = [[0] * (m+1) for _ in range(n+1)]

    max_len = 0  # Longitud maxima de la subcadena comun
    end_idx = 0  # Indice donde termina la subcadena en T1

    for i in range(1, n+1):
        for j in range(1, m+1):
            if T1[i-1] == T2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_idx = i  # Guardar el indice de fin
            else:
                dp[i][j] = 0

    # Extraer la subcadena comun mas larga
    lcs_str = T1[end_idx - max_len:end_idx]
    return lcs_str

T1 = "abcdfg"
T2 = "abdfg"
resultado = lcs(T1, T2)
print(f"La subcadena común más larga es: {resultado}")
