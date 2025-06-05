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
        score (int): É o tamanho do lcs (implementação opcional)
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
            float: A identidade do alinhamento em porcentagem.
        """
        self.alignment_length = len(self.aligned_seq1)
        identity = (self.score / self.alignment_length) * 100

        return identity
    
    def _identical_positions(self) -> list[int]:
        """
        Identifica as posições idênticas entre as sequências alinhadas.
        
        Returns:
            list[int]: Lista de posições onde os caracteres das sequências alinhadas são idênticos.
        """
        identical_positions = []
        if not self.seq3:
            for i, (a, b) in enumerate(zip(self.aligned_seq1, self.aligned_seq2), 1):
                if a == b:
                    identical_positions.append(i)
        else:
            for i, (a, b, c) in enumerate(zip(self.aligned_seq1, self.aligned_seq2, self.aligned_seq3), 1):
                if a == b == c:
                    identical_positions.append(i)
        return identical_positions
    
    def __str__(self) -> str:
        return "\n" \
        f"> Sequência 1: {" ".join(self.aligned_seq1)}\n" \
        f"> Sequência 2: {" ".join(self.aligned_seq2)}\n" \
        f"{f'> Sequência 3: {" ".join(self.aligned_seq3)}' if self.seq3 else ''}\n" \
        f"" \
        f"> Comprimento do alinhamento = {self.alignment_length}\n" \
        f"> Posições idênticas nas sequências (✓): {', '.join(map(str, self._identical_positions()))} → total = {self.score}\n" \
        f"> Identity = ({self.score} ÷ {self.alignment_length}) × 100 ≈ {self.identity():.2f}%\n"
