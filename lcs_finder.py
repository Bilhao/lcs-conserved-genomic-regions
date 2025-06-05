from sequence import Sequence
from sequence_alignment import SequenceAlignment


class LCSFinder():
    """
    Classe para encontrar a maior subsequência comum (LCS) entre duas ou três sequências.
    Esta classe utiliza programação dinâmica para calcular o LCS e reconstruir as sequências alinhadas.
    
    Attributes:
        seq1 (Sequence): A primeira sequência a ser comparada.
        seq2 (Sequence): A segunda sequência a ser comparada.
        seq3 (Sequence, optional): A terceira sequência a ser comparada. Se não for fornecida, o LCS será calculado apenas entre seq1 e seq2.
    """
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None):
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        matrix = self._dynamic_matrix_initialization()  # Inicializa a matriz dinâmica ou tensor
        matrix = self._dynamic_matrix_filled(matrix)  # Preenche a matriz dinâmica ou tensor
        lcs = self._lcs_reconstruction(matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)  # Alinha as sequencias 
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, len(lcs), self.seq3, aligned3 if self.seq3 else None)
        
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento da maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            int: O comprimento do LCS.
        """                
        matrix = self._dynamic_matrix_initialization()  # Inicializa a matriz dinâmica ou tensor
        matrix = self._dynamic_matrix_filled(matrix)  # Preenche a matriz dinâmica ou tensor
    
        return matrix[-1][-1] if self.seq3 is None else matrix[-1][-1][-1]  # Retorna o comprimento do LCS (último elemento da matriz/tensor)


    def _dynamic_matrix_initialization(self) -> list[list[int]] | list[list[list[int]]]:
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0 e tamanho (n+1) x (m+1):
        if self.seq3 is None:
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
            # return [[0 for _ in range(m+1)] for _ in range(n+1)]
        else:
            r1 = []
            i = 0
            while i < n + 1:
                r2 = []
                j = 0
                while j < m + 1:
                    r3 = []
                    w = 0
                    while w < k + 1:
                        r3.append(0)
                        w += 1
                    r2.append(r3) 
                    j += 1
                r1.append(r2)
                i += 1
            return r1
            # return [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]
    
    def _dynamic_matrix_filled(self, matrix: list[list[int]] | list[list[list[int]]]) -> list[list[int]] | list[list[list[int]]]:
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0
        
        # 2. Preenchimento da matriz ou tensor
        if self.seq3 is None:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        matrix[i][j] = matrix[i-1][j-1] + 1
                    else:
                        matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1])
        else:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    for w in range(1, k+1):
                        if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):
                            matrix[i][j][w] = matrix[i-1][j-1][w-1] + 1
                        else:
                            matrix[i][j][w] = max(matrix[i-1][j][w], matrix[i][j-1][w], matrix[i][j][w-1])
        return matrix  # Retorna a matriz preenchida ou o tensor preenchido
    
    def _lcs_reconstruction(self, matrix) -> str:
        lcs = "" 
        i = self.seq1.length()
        j = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 3. Reconstrução da subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        if not self.seq3:
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                else:
                    if matrix[i-1][j] >= matrix[i][j-1]:  # Se o valor de cima for maior ou igual, ir para o valor de cima
                        i -= 1 
                    else:  # Caso contrário, ir para o valor da esquerda
                        j -= 1
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, no caso foi escolhido ir para cima
            return lcs
        else:
            while i > 0 and j > 0 and w > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                    w -= 1
                else:
                    # Decide de qual direção está o maior valor no tensor
                    if matrix[i-1][j][w] >= matrix[i][j-1][w] and matrix[i-1][j][w] >= matrix[i][j][w-1]:
                        i -= 1  # Ir para cima
                    elif matrix[i][j-1][w] >= matrix[i-1][j][w] and matrix[i][j-1][w] >= matrix[i][j][w-1]:
                        j -= 1  # Ir para esquerda
                    else:
                        w -= 1  # Ir para frente
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, tanto para frente.
            return lcs

    def _sequence_alignment(self, lcs: str) -> tuple[str, str, str]:
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # Alinhamento das sequências       
        aligned1, aligned2, aligned3= "", "", ""  # Variáveis para armazenar os alinhamentos
        i, j, w = 0, 0, 0  # Índices para percorrer as sequências 
        l = 0  # Índice para percorrer a LCS
        if not self.seq3:
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:  # Se o caractere da seq1 não for igual ao caractere da LCS, adiciona traços
                    aligned1 += self.seq1.char_at(i)
                    aligned2 += "-"
                    i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:  # Se o caractere da seq2 não for igual ao caractere da LCS, adiciona traços
                    aligned1 += "-"
                    aligned2 += self.seq2.char_at(j)
                    j += 1
                aligned1 += self.seq1.char_at(i)  # Adiciona o caractere da LCS
                aligned2 += self.seq2.char_at(j)
                i += 1
                j += 1
                l += 1
            aligned1 += self.seq1.seq[i:] # Adiciona o restante da sequência seq1
            aligned2 += self.seq2.seq[j:] # Adiciona o restante da sequência seq2
            if len(aligned1) < len(aligned2):
                aligned1 += "-" * (len(aligned2) - len(aligned1))  # Preenche com traços se necessário
            elif len(aligned2) < len(aligned1):
                aligned2 += "-" * (len(aligned1) - len(aligned2))

        else: 
            ...
                
        return aligned1, aligned2, aligned3

    