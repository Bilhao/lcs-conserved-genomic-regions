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
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None): # type: ignore
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        ...
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento da maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            int: O comprimento do LCS.
        """
        ...
    

        