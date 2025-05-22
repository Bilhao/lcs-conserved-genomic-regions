def lcs_2_seq(seq1, seq2):
    n = len(seq1) # Linhas
    m = len(seq2) # Colunas

    # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0): 
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
    
    # Funcional
    def matriz_dinamica_FUN() -> list[list]:
        return [[0 for _ in range(m)] for _ in range(n)]
        
lcs_2_seq([1,2,3], [1,2,3,4,5])
