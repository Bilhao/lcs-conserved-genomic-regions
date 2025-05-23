def lcs_2_seq(seq1, seq2) -> str:
    n = len(seq1) + 1 # Núemro de linhas
    m = len(seq2) + 1 # Número de colunas

    # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0 e tamanho = (n+1)x(m+1)): 
    """
    # Recursiva
    def matriz_dinamica_REC(linhas=n) -> list[list]:
        if linhas == 0:
            return []
        else:
            return matriz_dinamica_REC(linhas - 1) + [[0] * m]

    # Imperativa
    def matriz_dinamica_IMP() -> list[list]:
        r1 = []
        i = 0
        while i < n:
            r2 = []
            j = 0
            while j < m:
                r2.append(0) 
                j += 1
            r1.append(r2)
            i += 1
        return r1
    """
    
    # Funcional
    def matriz_dinamica_FUN() -> list[list]:
        return [[0 for _ in range(m)] for _ in range(n)]


    # 2. Preenchimento da matriz

    # Imperativa
    def matriz_preenchida_IMP(matriz) -> list[list]:
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
        i = n - 1  # Variáveis de incremento iniciadas em n - 1 pois a indexação começa em 0 até n - 1 (n - 1 é o último elemento)
        j = m - 1
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                r = seq1[i-1] + r
                i -= 1
                j -= 1
            else:
                if matriz[i-1][j] > matriz[i][j-1]:  # Se o valor de cima for maior, ir para o valor de cima
                    i -= 1
                elif matriz[i-1][j] < matriz[i][j-1]:  # Se o valor da esquerda for maior, ir para o valor da esquerda
                    j -= 1
                else:
                    i -= 1  # Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda
        return r


    matriz = matriz_dinamica_FUN() # Matriz dinâmica
    matriz_preenchida = matriz_preenchida_IMP(matriz) # Matriz preenchida

    return reconstrucao_IMP(matriz_preenchida)


"""seq1 = input("Primeira sequência: ")
seq2 = input("Segunda sequência: ")
lcs = lcs_2_seq(seq1, seq2)
print(lcs)"""


def lcs_3_seq(seq1, seq2, seq3):
    n = len(seq1) + 1
    m = len(seq2) + 1
    k = len(seq3) + 1

    # 1. Inicialização do tensor (todos os valores iguais a 0 e tamanho = (n+1)x(m+1)x(k+1)): 

    # Recursiva
    def tensor_REC(linhas=n) -> list:
        if linhas == 0:
            return []
        else:
            def rec_colunas(colunas=m) -> list:
                if colunas == 0:
                    return []
                else:
                    def rec_profundidade(profundidade=k) -> list:
                        if profundidade == 0:
                            return []
                        else:
                            return rec_profundidade(profundidade - 1) + [0]
                    return rec_colunas(colunas - 1) + [rec_profundidade()]
            return tensor_REC(linhas - 1) + [rec_colunas()]

    # Imperativa
    def tensor_IMP() -> list[list]:
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
    def tensor_FUN() -> list[list]:
        return [[[0 for _ in range(k)] for _ in range(m)] for _ in range(n)]

lcs_3_seq("AGG", "GXT", "AGG")