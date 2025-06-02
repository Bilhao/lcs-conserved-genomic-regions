class Sequence():
    """
    Classe que representa uma sequência biológicas (DNA, RNA ou proteína).

    Attributes:
        id (str): Identificador.
        description (str): Descrição da sequência.
        seq (str): A sequência de nucleotídeos ou aminoácidos.
    """
    def __init__(self, id: str, description: str,  seq: str):
        self.id = id
        self.description = description  #malta tf é a description tou atoa -> é o que a sequencia é, tipo a doença que vamos escolher ou alguma outra coisa que ela representa
        self.seq = seq

    def length(self) -> int:
        """
        Calcula o comprimento da sequência.

        Returns:
            int: O comprimento da sequência.
        """
        return len(self.seq)
        
    
    def char_at(self, position: int) -> str:
        """
        Retorna o caractere na posição especificada da sequência.

        Parameters:
            position (int): A posição do caractere na sequência.

        Returns:
            str: O caractere na posição especificada.
        """
        return self.seq[position]
        
    
    def __str__(self) -> str:
        return "" \
        f"> Id: {self.id}\n" \
        f"> Descrição: {self.description}\n" \
        f"> Sequência: {self.seq}\n"


