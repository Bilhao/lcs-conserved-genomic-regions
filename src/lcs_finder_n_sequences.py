from .sequence import Sequence
from itertools import product

class LCSFinderNSequences():
    """
    Classe para encontrar a subsequência comum mais longa (LCS) entre N sequências.

    Attributes:
        sequences (list[Sequence]): Lista de objetos Sequence representando as sequências a serem comparadas.
    """
    def __init__(self, sequences: list[Sequence]):
        self.sequences = sequences

        self.dd = self._initialization()
        self.dd = self._filling(self.dd)
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento do LCS (Longest Common Subsequence) para N sequências.

        Returns:
            int: Comprimento do LCS para as N sequências.
        """
        return self.dd[tuple(seq.length() for seq in self.sequences)]
    
    def get_lcs(self) -> str:
        """
        Obtém o LCS (Longest Common Subsequence) para N sequências.

        Returns:
            str: O LCS formado pelas N sequências.
        """
        indices = [seq.length() for seq in self.sequences]
        lcs_chars = []

        while all(i > 0 for i in indices):
            chars = [self.sequences[i].seq[indices[i] - 1] for i in range(len(self.sequences))]
            if all(c == chars[0] for c in chars):
                lcs_chars.append(chars[0])
                indices = [i - 1 for i in indices]
            else:
                max_index = max(range(len(indices)), key=lambda i: self.dd[tuple(indices[:i] + [indices[i] - 1] + indices[i + 1:])] if indices[i] > 0 else -1)
                indices[max_index] -= 1

        return ''.join(reversed(lcs_chars))
    
    def compute_lcs(self):
        """
        Para compatibilidade com LCSFinder - retorna um objeto simples com aligned sequences.
        """
        from .sequence_alignment import SequenceAlignment
        lcs = self.get_lcs()
        # Para N sequências, apenas retornamos as primeiras 3 alinhadas (limitação atual)
        if len(self.sequences) >= 2:
            seq1, seq2 = self.sequences[0], self.sequences[1]
            seq3 = self.sequences[2] if len(self.sequences) > 2 else None
            # Alinhamento simples baseado na LCS
            aligned_seq1 = seq1.seq
            aligned_seq2 = seq2.seq
            aligned_seq3 = seq3.seq if seq3 else None
            return SequenceAlignment(seq1, seq2, aligned_seq1, aligned_seq2, len(lcs), seq3, aligned_seq3)
        return None

    def _initialization(self):
        """
        Inicializa um dicionário dinâmico (dd) para o cálculo do LCS de N sequências.
        """
        lengths = [seq.length() for seq in self.sequences]
        n = len(self.sequences)
        dd = {}

        def fill(indices):
            if len(indices) == n:
                dd[tuple(indices)] = 0
                return
            for i in range(lengths[len(indices)] + 1):
                fill(indices + [i])

        fill([])
        return dd

    def _filling(self, dd) -> dict:
        """
        Preenche o dicionário dinâmico (dd) com os valores do LCS para todas as combinações de índices.

        Parameters:
            dd (dict): Dicionário dinâmico inicializado com zeros.

        Returns:
            dict: Dicionário preenchido com os comprimentos do LCS.
        """
        lengths = [seq.length() for seq in self.sequences]
        n = len(self.sequences)

        for indices in product(*[range(1, l + 1) for l in lengths]):
            chars = [self.sequences[i].seq[indices[i] - 1] for i in range(n)] 

            if all(c == chars[0] for c in chars):
                prev_indices = tuple(idx - 1 for idx in indices)
                dd[indices] = dd[prev_indices] + 1
            else:
                max_val = 0
                for i in range(n):
                    reduced_indices = list(indices)
                    reduced_indices[i] -= 1
                    if reduced_indices[i] >= 0:
                        max_val = max(max_val, dd[tuple(reduced_indices)])
                dd[indices] = max_val
        return dd
