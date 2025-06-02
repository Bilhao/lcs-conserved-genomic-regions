from sequence import Sequence

class SequenceAlignment():
    """
    Classe que representa o alinhamento de duas ou três sequências.
    Esta classe armazena as sequências originais, as sequências alinhadas e o escore do alinhamento.

    Attributes:
        seq1 (Sequence): A primeira sequência a ser alinhada.
        seq2 (Sequence): A segunda sequência a ser alinhada.
        seq3 (Sequence, optional): A terceira sequência a ser alinhada. Se não for fornecida, o alinhamento será entre seq1 e seq2.
        aligned_seq1 (str): A primeira sequência após reconstrução e alinhamento.
        aligned_seq2 (str): A segunda sequência após reconstrução e alinhamento.
        aligned_seq3 (str, optional): A terceira sequência após o alinhamento. Se não for fornecida, não será usada no alinhamento.
        score (int): É o comprimento do alinhamento (implementação opcional)
    """
    def __init__(self, seq1: Sequence, seq2: Sequence, aligned_seq1: str, aligned_seq2: str, score: int, seq3: Sequence = None, aligned_seq3: str = None): # type: ignore
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        self.aligned_seq1 = aligned_seq1
        self.aligned_seq2 = aligned_seq2
        self.aligned_seq3 = aligned_seq3
        self.score = score
        
    def identity(self) -> float:
        """
        Calcula a identidade do alinhamento, que é a proporção de caracteres idênticos entre as sequências alinhadas.
        Returns:
            float: A identidade do alinhamento, entre 0 e 1.
        """
        ...
    
    def __str__(self) -> str:
        ...
