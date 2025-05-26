from sequence import Sequence
from sequence_alignment import SequenceAlignment

class LCSFinder():
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None): # type: ignore
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
    
    def compute_lcs(self) -> SequenceAlignment:
        ...
    
    def get_lcs_length(self) -> int:
        ...
    

        