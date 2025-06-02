def lcs_2_seq(seq1, seq2) -> str:
    n = len(seq1) # Número de linhas (tamanho da sequência)
    m = len(seq2) # Número de colunas (tamanho da sequência)

    # Imperativa
    def matriz_dinamica_IMP() -> list[list[int]]:
        r1 = []
        i = 0
        while i < n + 1:
            r2 = []
            j = 0
            while j < m + 1:
                r2.append(0) 
                j += 1
            r1.append(r2)
            i += 1
        return r1
    
    # Funcional
    def matriz_dinamica_FUN() -> list[list]:
        return [[0 for _ in range(m)] for _ in range(n)]


    # 2. Preenchimento da matriz
    def matriz_preenchida_IMP(matriz) -> list[list[int]]:
        i = 1  # Variável de incremento "i" iniciada em 1 pois a primeira linha é preenchida por zeros
        while i < n:  
            j = 1  # Variável de incremento "j" iniciada em 1 pois a primeira coluna é preenchida por zeros 
            while j < m:
                if seq1[i-1] == seq2[j-1]:
                    matriz[i][j] = matriz[i-1][j-1] + 1  # Se for igual, será igual ao valor da diagonal anterior + 1
                else:
                    matriz[i][j] = max(matriz[i-1][j], matriz[i][j-1])  # Se não for igual, será o máximo dos valores acima e a esquerda
                j += 1
            i += 1
        return matriz

    # 3. Reconstrução da solução
    def reconstrucao_IMP(matriz) -> str:
        r = "" 
        i = n - 1  # Variáveis de incremento iniciadas em "n - 1" pois a indexação começa em 0 até "n - 1" (n - 1 é o último elemento)
        j = m - 1
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                r = seq1[i-1] + r
                i -= 1
                j -= 1
            else:
                if matriz[i-1][j] >= matriz[i][j-1]:  # Se o valor de cima for maior, ir para o valor de cima
                    i -= 1 
                else:  # Caso contrário, ir para o valor da esquerda
                    j -= 1
                # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda
        return r

    # 4. Identity
    def identity():
        ...

    matriz = matriz_dinamica_FUN() # Matriz dinâmica
    matriz_preenchida = matriz_preenchida_IMP(matriz) # Matriz preenchida
    return reconstrucao_IMP(matriz_preenchida)


def lcs_3_seq(seq1, seq2, seq3):
    n = len(seq1) + 1
    m = len(seq2) + 1
    k = len(seq3) + 1

    # 1. Inicialização do tensor (todos os valores iguais a 0 e tamanho = (n+1)x(m+1)x(k+1)): 
    # Recursiva - Não consegui fazer isso ainda. Pensando...
    def tensor_REC() -> list[list[list[int]]]:
        ...

    # Imperativa
    def tensor_IMP() -> list[list[list[int]]]:
        r1 = []
        i = 0
        while i < n:
            r2 = []
            j = 0
            while j < m:
                r3 = []
                w = 0
                while w < k:
                    r3.append(0)
                    w += 1
                r2.append(r3)
                j += 1
            r1.append(r2)
            i += 1
        return r1

    # Funcional
    def tensor_FUN() -> list[list[list[int]]]:
        return [[[0 for _ in range(k)] for _ in range(m)] for _ in range(n)]


    # 2. Preenchimento do tensor
    def tensor_preenchido_IMP(tensor) -> list[list[list[int]]]:
        i = 1
        while i < n:
            j = 1
            while j < m:
                w = 1
                while w < k:
                    if seq1[i-1] == seq2[j-1] == seq3[w-1]:
                        tensor[i][j][w] = tensor[i-1][j-1][w-1] + 1
                    else:
                        tensor[i][j][w] = max(tensor[i-1][j][w], tensor[i][j-1][w], tensor[i][j][w-1])
                    w += 1
                j += 1
            i += 1
        return tensor
    
    # 3. Reconstrução da solução
    def reconstrucao_IMP(tensor) -> str:
        r = ""
        i = n - 1  # Variáveis de incremento iniciadas em "n - 1" pois a indexação começa em 0 até "n - 1" (n - 1 é o último elemento)
        j = m - 1
        w = k - 1
        while i > 0 and j > 0 and w > 0:
            if seq1[i-1] == seq2[j-1] == seq3[w-1]:
                r = seq1[i-1] + r
                i -= 1
                j -= 1
                w -= 1
            else:
                # Decide de qual direção está o maior valor no tensor
                if tensor[i-1][j][w] >= tensor[i][j-1][w] and tensor[i-1][j][w] >= tensor[i][j][w-1]:
                    i -= 1  # Move na primeira sequência
                elif tensor[i][j-1][w] >= tensor[i-1][j][w] and tensor[i][j-1][w] >= tensor[i][j][w-1]:
                    j -= 1  # Move na segunda sequência
                else:
                    w -= 1  # Move na terceira sequência
        return r
    
    # 4. Identity
    def identity():
        ...
    
    tensor = tensor_FUN()
    tensor_preenchido = tensor_preenchido_IMP(tensor)
    return reconstrucao_IMP(tensor_preenchido)


if __name__ == "__main__":
    seq1 = input("Primeira sequência: ")
    seq2 = input("Segunda sequência: ")
    lcs2 = lcs_2_seq(seq1, seq2)
    print(lcs2, "\n")

    seq1 = input("Primeira sequência: ")
    seq2 = input("Segunda sequência: ")
    seq3 = input("Terceira sequência: ")
    lcs3 = lcs_3_seq(seq1, seq2, seq3)
    print(lcs3)