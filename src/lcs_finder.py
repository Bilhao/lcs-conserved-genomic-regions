from .sequence import Sequence
from .sequence_alignment import SequenceAlignment


class LCSFinder():
    """
    Classe para encontrar a maior subsequência comum (LCS) entre duas ou três sequências.
    Esta classe utiliza programação dinâmica para calcular o LCS e reconstruir as sequências alinhadas.
    
    Attributes:
        seq1 (Sequence): A primeira sequência a ser comparada.
        seq2 (Sequence): A segunda sequência a ser comparada.
        seq3 (Sequence, optional): A terceira sequência a ser comparada.
    """
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None):
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        
        self.dp = self._initialization()
        self.dp = self._filling(self.dp)
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        lcs = self._lcs_reconstruction(self.dp)
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)
        
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
        lcs = self._lcs_reconstruction(self.dp)
        return lcs

    def _initialization(self) -> list[list[int]] | list[list[list[int]]]:
        """
        Inicializa a matriz dinâmica ou tensor para armazenar os valores de LCS.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor inicializado com zeros.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        if self.seq3 is None:
            return [[0 for _ in range(m+1)] for _ in range(n+1)]
        else:
            return [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]

    def _filling(self, dp: list[list[int]] | list[list[list[int]]]) -> list[list[int]] | list[list[list[int]]]:
        """
        Preenche a matriz dinâmica ou tensor com os valores de LCS usando programação dinâmica.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor inicializado.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor preenchido.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0
        
        if self.seq3 is None:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        else:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    for w in range(1, k+1):
                        if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):
                            dp[i][j][w] = dp[i-1][j-1][w-1] + 1
                        else:
                            dp[i][j][w] = max(dp[i-1][j][w], dp[i][j-1][w], dp[i][j][w-1])
        return dp
    
    def _lcs_reconstruction(self, dp) -> str:
        """
        Reconstrói a subsequência comum mais longa (LCS) a partir da matriz dinâmica ou tensor.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor preenchido.
        
        Returns:
            str: A subsequência comum mais longa (LCS).
        """
        lcs = "" 
        i = self.seq1.length()
        j = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        if not self.seq3:
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                    lcs = self.seq1.char_at(i-1) + lcs 
                    i -= 1
                    j -= 1
                else:
                    if dp[i-1][j] >= dp[i][j-1]:
                        i -= 1 
                    else:
                        j -= 1
            return lcs
        else:
            while i > 0 and j > 0 and k > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(k-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                    k -= 1
                else:
                    if dp[i-1][j][k] >= dp[i][j-1][k] and dp[i-1][j][k] >= dp[i][j][k-1]:
                        i -= 1
                    elif dp[i][j-1][k] >= dp[i-1][j][k] and dp[i][j-1][k] >= dp[i][j][k-1]:
                        j -= 1
                    else:
                        k -= 1
            return lcs

    def _sequence_alignment(self, lcs: str) -> tuple[str, str, str]:
        """
        Alinha as sequências com base na subsequência comum mais longa (LCS) reconstruída.
        
        Parameters:
            lcs (str): A subsequência comum mais longa (LCS).
        
        Returns:
            tuple[str, str, str]: As sequências alinhadas (seq1, seq2, seq3) com base na LCS.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        w = self.seq3.length() if self.seq3 else 0

        aligned1, aligned2, aligned3= "", "", ""
        i, j, k = 0, 0, 0
        l = 0
        if not self.seq3:
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:
                    aligned1 += self.seq1.char_at(i)
                    aligned2 += "-"
                    i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:
                    aligned1 += "-"
                    aligned2 += self.seq2.char_at(j)
                    j += 1
                aligned1 += self.seq1.char_at(i)
                aligned2 += self.seq2.char_at(j)
                i += 1
                j += 1
                l += 1
            aligned1 += self.seq1.seq[i:]
            aligned2 += self.seq2.seq[j:]
            if len(aligned1) < len(aligned2):
                aligned1 += "-" * (len(aligned2) - len(aligned1))
            if len(aligned2) < len(aligned1):
                aligned2 += "-" * (len(aligned1) - len(aligned2))

        else: 
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:
                    if j < m and self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif k < w and self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif j < m and k < w and self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    else: 
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += "-"
                        i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:
                    if i < n and self.seq2.char_at(j) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif k < w and self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif i < n and k < w and self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    else:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        j += 1
                while k < w and self.seq3.char_at(k) != lcs[l]:
                    if i < n and self.seq3.char_at(k) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif j < m and self.seq3.char_at(k) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif i < n and j < m and self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    else:
                        aligned1 += "-"
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        k += 1
                aligned1 += self.seq1.char_at(i)
                aligned2 += self.seq2.char_at(j)
                aligned3 += self.seq3.char_at(k)
                i += 1
                j += 1
                k += 1
                l += 1

            aligned1 += self.seq1.seq[i:]
            aligned2 += self.seq2.seq[j:]
            aligned3 += self.seq3.seq[k:]

            max_length = max(len(aligned1), len(aligned2), len(aligned3))
            if len(aligned1) < max_length:
                aligned1 += "-" * (max_length - len(aligned1))
            if len(aligned2) < max_length:
                aligned2 += "-" * (max_length - len(aligned2))
            if len(aligned3) < max_length:
                aligned3 += "-" * (max_length - len(aligned3))

        return aligned1, aligned2, aligned3
