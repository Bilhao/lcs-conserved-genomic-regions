from sequence import Sequence

class SequenceAlignment():
    def __init__(self, seq1: Sequence, seq2: Sequence, aligned_seq1: str, aligned_seq2: str, score: int, seq3: Sequence = None, aligned_seq3: str = None): # type: ignore
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        self.aligned_seq1 = aligned_seq1
        self.aligned_seq2 = aligned_seq2
        self.aligned_seq3 = aligned_seq3
        self.score = score
        
    def identity(self) -> float:
        ...
    
    def __str__(self) -> str:
        ...
