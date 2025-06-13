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
        
        self.dp = self._initialization()  # Inicializa a matriz dinâmica ou tensor
        self.dp = self._filling(self.dp)  # Preenche a matriz dinâmica ou tensor
    
    def compute_lcs(self)   -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        lcs = self._lcs_reconstruction(self.dp)  # Reconstrói a subsequência comum mais longa (LCS)
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)  # Alinha as sequencias 
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, len(lcs), self.seq3, aligned3 if self.seq3 else None)
        
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento da maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            int: O comprimento do LCS.
        """
        if self.seq3 is None:
            return self.dp[-1][-1]
        else:
            return self.dp[-1][-1][-1]

    def get_lcs(self) -> str:
        """
        Obtém a maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            str: A LCS reconstruída.
        """
        lcs = self._lcs_reconstruction(self.dp)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        return lcs  # Retorna a LCS reconstruída a partir da matriz dinâmica ou tensor preenchido

    def _initialization(self) -> list[list[int]] | list[list[list[int]]]:
        """
        Inicializa a matriz dinâmica ou tensor para armazenar os valores de LCS.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor inicializado com zeros.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0 e tamanho (n+1) x (m+1):
        # A primeira coluna e linha são sempre preenchidas por 0.
        if self.seq3 is None:
            return [[0 for _ in range(m+1)] for _ in range(n+1)]
        else:
            return [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]

    def _filling(self, dp: list[list[int]] | list[list[list[int]]]) -> list[list[int]] | list[list[list[int]]]:
        """
        Preenche a matriz dinâmica ou tensor com os valores de LCS usando programação dinâmica.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor inicializado com zeros.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor preenchido com os valores de LCS.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0
        
        # 2. Preenchimento da matriz ou tensor
        if self.seq3 is None:
            for i in range(1, n+1):  # Não inclui o 0 da primeira coluna
                for j in range(1, m+1):  # Não inclui o 0 da primeira coluna
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        dp[i][j] = dp[i-1][j-1] + 1  # Adiciona 1 à diagonal anterior se os caracteres forem iguais
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Retorna o máximo entre entrada superior e a entrada à esquerda
        else:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    for w in range(1, k+1):
                        if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):
                            dp[i][j][w] = dp[i-1][j-1][w-1] + 1
                        else:
                            dp[i][j][w] = max(dp[i-1][j][w], dp[i][j-1][w], dp[i][j][w-1])
        return dp  # Retorna a matriz preenchida ou o tensor preenchido
    
    def _lcs_reconstruction(self, dp) -> str:
        """
        Reconstrói a subsequência comum mais longa (LCS) a partir da matriz dinâmica ou tensor preenchido.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor preenchido com os valores de LCS.
        
        Returns:
            str: A subsequência comum mais longa (LCS).
        """
        lcs = "" 
        i = self.seq1.length()
        j = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 3. Reconstrução da subsequência comum mais longa (LCS)
        if not self.seq3:
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                    lcs = self.seq1.char_at(i-1) + lcs 
                    i -= 1
                    j -= 1
                else:
                    if dp[i-1][j] >= dp[i][j-1]:  # Se o valor de cima for maior ou igual, ir para o valor de cima
                        i -= 1 
                    else:  # Caso contrário, ir para o valor da esquerda
                        j -= 1
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, no caso foi escolhido ir para cima
            return lcs
        else:
            while i > 0 and j > 0 and k > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(k-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                    k -= 1
                else:
                    # Decide de qual direção está o maior valor no tensor
                    if dp[i-1][j][k] >= dp[i][j-1][k] and dp[i-1][j][k] >= dp[i][j][k-1]:
                        i -= 1  # Ir para cima
                    elif dp[i][j-1][k] >= dp[i-1][j][k] and dp[i][j-1][k] >= dp[i][j][k-1]:
                        j -= 1  # Ir para esquerda
                    else:
                        k -= 1  # Ir para frente
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, tanto para frente.
            return lcs

    def _sequence_alignment(self, lcs: str) -> tuple[str, str, str]:
        """
        Alinha as sequências com base na subsequência comum mais longa (LCS) reconstruída.
        
        Parameters:
            lcs (str): A subsequência comum mais longa (LCS) reconstruída a partir da matriz dinâmica ou tensor preenchido.
        
        Returns:
            tuple[str, str, str]: As sequências alinhadas (seq1, seq2, seq3) com base na LCS.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        w = self.seq3.length() if self.seq3 else 0

        # Alinhamento das sequências       
        aligned1, aligned2, aligned3= "", "", ""  # Variáveis para armazenar os alinhamentos
        i, j, k = 0, 0, 0  # Índices para percorrer as sequências 
        l = 0  # Índice para percorrer a LCS
        if not self.seq3:
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:  # Se o caractere da seq1 não for igual ao caractere da LCS, adiciona traços
                    aligned1 += self.seq1.char_at(i)
                    aligned2 += "-"
                    i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:
                    aligned1 += "-"
                    aligned2 += self.seq2.char_at(j)
                    j += 1
                aligned1 += self.seq1.char_at(i)  # Adiciona o caractere da LCS
                aligned2 += self.seq2.char_at(j)
                i += 1
                j += 1
                l += 1
            aligned1 += self.seq1.seq[i:]  # Adiciona o restante da sequência seq1
            aligned2 += self.seq2.seq[j:]
            if len(aligned1) < len(aligned2):
                aligned1 += "-" * (len(aligned2) - len(aligned1))  # Preenche com traços se necessário
            if len(aligned2) < len(aligned1):
                aligned2 += "-" * (len(aligned1) - len(aligned2))

        else: 
            # Alinhamento para três sequências usando a LCS reconstruída
            while l < len(lcs):
                # Avança nas três sequências até encontrar o próximo caractere da LCS em cada uma.
                while i < n and self.seq1.char_at(i) != lcs[l]:
                    # Casos onde dois caracteres coincidem, mas não são o da LCS.
                    if self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    else: 
                        # Caso nenhum caractere coincida, adiciona apenas o caractere da seq1 e traços.
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += "-"
                        i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:
                    # Casos onde dois caracteres coincidem, mas não são o da LCS.
                    if self.seq2.char_at(j) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    else:
                        # Caso nenhum caractere coincida, adiciona apenas o caractere da seq2 e traços.
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        j += 1
                while k < w and self.seq3.char_at(k) != lcs[l]:
                    # Casos onde dois caracteres coincidem, mas não são o da LCS.
                    if self.seq3.char_at(k) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif self.seq3.char_at(k) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    else:
                        # Caso nenhum caractere coincida, adiciona apenas o caractere da seq3 e traços
                        aligned1 += "-"
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        k += 1
                # Adiciona o caractere da LCS nas três sequências
                aligned1 += self.seq1.char_at(i)
                aligned2 += self.seq2.char_at(j)
                aligned3 += self.seq3.char_at(k)
                i += 1
                j += 1
                k += 1
                l += 1

            # Adiciona o restante das sequências (caso alguma seja maior).
            aligned1 += self.seq1.seq[i:] # Adiciona o restante da sequência seq1.
            aligned2 += self.seq2.seq[j:]
            aligned3 += self.seq3.seq[k:]

            # Ajusta o comprimento das sequências alinhadas para que fiquem iguais, preenchendo com traços se necessário.
            max_length = max(len(aligned1), len(aligned2), len(aligned3))
            min_length = min(len(aligned1), len(aligned2), len(aligned3))

            while min_length < max_length:
                # Verifica se aligned1 é menor que o comprimento máximo
                if len(aligned1) < max_length:
                    # Se algum índice da sequência (i, j, k) chegou ao fim da respetiva sequência (n, m, w), preenche aligned1 com lacunas ("-") até atingir max_length
                    if i == n or j == m or k == w:
                        aligned1 += "-" * (max_length - len(aligned1))
                    elif self.seq1.char_at(i) != self.seq2.char_at(j) and self.seq2.char_at(j) == self.seq3.char_at(k):
                        aligned1 = aligned1[:i] + "-" + aligned1[i:]
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) != self.seq2.char_at(j) and self.seq1.char_at(i) == self.seq3.char_at(k):
                        aligned1 = aligned1[:i+1] + "-" + aligned1[i+1:]
                        j += 1
                        k += 1
                if len(aligned2) < max_length:
                    if i == n or j == m or k == w:
                        aligned2 += "-" * (max_length - len(aligned2))
                    elif self.seq2.char_at(j) != self.seq1.char_at(i) and self.seq1.char_at(i) == self.seq3.char_at(k):
                        aligned2 = aligned2[:j] + "-" + aligned2[j:]
                        i += 1
                        k += 1
                    elif self.seq2.char_at(j) != self.seq1.char_at(i) and self.seq2.char_at(j) == self.seq3.char_at(k):
                        aligned2 = aligned2[:j+1] + "-" + aligned2[j+1:]
                        i += 1
                        k += 1
                if len(aligned3) < max_length:
                    if i == n or j == m or k == w:
                        aligned3 += "-" * (max_length - len(aligned3))
                    elif self.seq3.char_at(k) != self.seq1.char_at(i) and self.seq1.char_at(i) == self.seq2.char_at(j):
                        aligned3 = aligned3[:k] + "-" + aligned3[k:]
                        i += 1
                        j += 1
                    elif self.seq3.char_at(k) != self.seq1.char_at(i) and self.seq3.char_at(k) == self.seq2.char_at(j):
                        aligned3 = aligned3[:k+1] + "-" + aligned3[k+1:]
                        i += 1
                        j += 1

                # Atualiza max_length e min_length com base nos comprimentos atuais das sequências alinhadas
                max_length = max(len(aligned1), len(aligned2), len(aligned3))
                min_length = min(len(aligned1), len(aligned2), len(aligned3))

        return aligned1, aligned2, aligned3