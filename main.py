def lcs_2_seq(seq1, seq2):
    n = len(seq1) + 1 # Núemro de linhas
    m = len(seq2) + 1 # Número de colunas

    # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0 e tamanho = (n+1)x(m+1)): 

    """
    # Recursiva
    def matriz_dinamica_REC(linhas=n) -> list[list]:
        if linhas == 0:
            return []
        else:
            return matriz_dinamica_REC(linhas - 1) + [[0] * (m)]

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
    def matriz_preenchida_IMP(md) -> list[list]:
        i = 1  # Variável de incremento "i" iniciada em 1 pois a primeira linha é preenchida por zeros
        while i < n:  
            j = 1  # Variável de incremento "j" iniciada em 1 pois a primeira coluna é preenchida por zeros 
            while j < m:
                if seq1[i-1] == seq2[j-1]:
                    md[i][j] = md[i-1][j-1] + 1  # Se for igual: Será igual ao valor da diagonal anterior + 1
                else:
                    md[i][j] = max(md[i-1][j], md[i][j-1])  # Se não for igual: Será o máximo dos valores acima e a esquerda
                j += 1
            i += 1
        return md

    # 3. Reconstrução da solução
    def reconstrucao_IMP(mp) -> str:
        r = "" 
        i = n - 1  # Variáveis de incremento iniciadas em n - 1 pois 
        j = m - 1
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                r = seq1[i-1] + r
                i -= 1
                j -= 1
            else:
                if mp[i-1][j] > mp[i][j-1]:  # Se o valor de cima for maior, ir para o valor de cima
                    i -= 1
                elif mp[i-1][j] < mp[i][j-1]:  # Se o valor da esquerda for maior, ir para o valor da esquerda
                    j -= 1
                else:
                    j -= 1  # Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda
        return r


    md = matriz_dinamica_FUN() # Matriz dinâmica
    mp = matriz_preenchida_IMP(md) # Matriz preenchida
    print(mp)
    print(reconstrucao_IMP(mp))



lcs_2_seq("ATGCTGA", "TGCTAGC")

