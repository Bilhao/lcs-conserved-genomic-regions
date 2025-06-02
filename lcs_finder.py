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
        aligned1, aligned2, aligned3, score = self._subsequence_reconstruction(matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, score, self.seq3, aligned3 if self.seq3 else None)
        
    
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
    
    def _subsequence_reconstruction(self, matrix):
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 3. Reconstrução da subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido       
        aligned1, aligned2, aligned3= "", "", ""  # Variáveis para armazenar os alinhamentos
        i, j, w = n, m, k  # Começa do final da matriz

        if not self.seq3:
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):  # Se os caracteres forem iguais, adiciona ao alinhamento e vai para a diagonal
                    aligned1 = self.seq1.char_at(i-1) + aligned1
                    aligned2 = self.seq2.char_at(j-1) + aligned2
                    i -= 1
                    j -= 1
                else: 
                    if matrix[i-1][j] > matrix[i][j-1]: # Se o valor de cima for maior, ir para o valor de cima
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        i -= 1
                    elif matrix[i-1][j] < matrix[i][j-1]: # Se o valor da esquerda for maior, ir para o valor da esquerda
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        j -= 1
                    else: 
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        i -= 1
                        j -= 1
        else: 
            while i > 0 and j > 0 and w > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):  # Se os caracteres forem iguais, adiciona ao alinhamento
                    aligned1 = self.seq1.char_at(i-1) + aligned1
                    aligned2 = self.seq2.char_at(j-1) + aligned2
                    aligned3 = self.seq3.char_at(w-1) + aligned3
                    i -= 1
                    j -= 1
                    w -= 1
                else:
                    if matrix[i-1][j][w] > matrix[i][j-1][w] > matrix[i][j][w-1] or matrix[i-1][j][w] > matrix[i][j][w-1] > matrix[i][j-1][w]:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = "-" + aligned3
                        i -= 1
                    elif matrix[i][j-1][w] > matrix[i-1][j][w] > matrix[i][j][w-1] or matrix[i][j-1][w] > matrix[i][j][w-1] > matrix[i-1][j][w]:
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = "-" + aligned3
                        j -= 1
                    elif matrix[i][j][w-1] > matrix[i-1][j][w] > matrix[i][j-1][w] or matrix[i][j][w-1] > matrix[i][j-1][w] > matrix[i-1][j][w]:
                        aligned1 = "-" + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = self.seq3.char_at(w-1) + aligned3
                        w -= 1
                    elif matrix[i-1][j][w] == matrix[i][j-1][w] > matrix[i][j][w-1]:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = "-" + aligned3
                        i -= 1
                        j -= 1
                    elif matrix[i-1][j][w] == matrix[i][j][w-1] > matrix[i][j-1][w]:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = self.seq3.char_at(w-1) + aligned3
                        i -= 1
                        w -= 1
                    elif matrix[i][j-1][w] == matrix[i][j][w-1] > matrix[i-1][j][w]:
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = self.seq3.char_at(w-1) + aligned3
                        j -= 1
                        w -= 1
                    elif matrix[i-1][j][w] == matrix[i][j-1][w] < matrix[i][j][w-1]:
                        aligned1 = "-" + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = self.seq3.char_at(w-1) + aligned3
                        w -= 1
                    elif matrix[i-1][j][w] == matrix[i][j][w-1] < matrix[i][j-1][w]:
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = "-" + aligned3
                        j -= 1
                    elif matrix[i][j-1][w] == matrix[i][j][w-1] < matrix[i-1][j][w]:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = "-" + aligned3
                        i -= 1
                    else:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = self.seq3.char_at(w-1) + aligned3
                        i -= 1
                        j -= 1
                        w -= 1
                
        return aligned1, aligned2, aligned3, matrix[n][m] if not self.seq3 else matrix[n][m][k]

    