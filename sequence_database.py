from sequence import Sequence

class SequenceDatabase():
    def __init__(self):
        ...

    def add_sequence(self, sequence: Sequence):
        ...
    
    def get_sequence_by_id(self, id: str) -> Sequence:
        ...

    def load_from_fasta(self, filename: str):
        ...
        