class Sequence():
    def __init__(self, id: str, description: str,  seq: str):
        self.id = id
        self.description = description  #malta tf é a description tou atoa
        self.seq = seq

    def length(self) -> int:
        ...
    
    def char_at(self, position: int) -> str:
        ...
    
    def __str__(self) -> str:
        return self.seq


