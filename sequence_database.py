from sequence import Sequence

class SequenceDatabase():
    """
    Classe que representa um banco de dados de sequências.
    Esta classe permite adicionar sequências, buscar sequências por ID e carregar sequências de um arquivo FASTA.
    """
    def __init__(self):
        ...

    def add_sequence(self, sequence: Sequence):
        """
        Adiciona uma sequência ao banco de dados.
        Parameters:
            sequence (Sequence): A sequência a ser adicionada.
        """
        ...
    
    def get_sequence_by_id(self, id: str) -> Sequence:
        """
        Busca uma sequência pelo seu ID.
        Parameters:
            id (str): O ID da sequência a ser buscada.
        Returns:
            Sequence: A sequência correspondente ao ID fornecido.
        Raises:
            KeyError: Se a sequência com o ID fornecido não for encontrada.
        """
        ...

    def load_from_fasta(self, filename: str):
        """
        Carrega sequências de um arquivo FASTA e as adiciona ao banco de dados.
        Parameters:
            filename (str): O caminho do arquivo FASTA a ser carregado.
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado.
            ValueError: Se o arquivo não estiver no formato FASTA válido.
        """
        ...
        