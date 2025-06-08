from sequence import Sequence

class SequenceDatabase():
    """
    Classe que representa um banco de dados de sequências.
    Esta classe permite adicionar sequências, buscar sequências por ID e carregar sequências de um arquivo FASTA.
    """
    def __init__(self):
        self.database = {}

    def add_sequence(self, sequence: Sequence):
        """
        Adiciona uma sequência ao banco de dados. 
        A sequência só será adicionada se tiver um ID, descrição e sequência válidos, e se o ID não estiver já presente no banco de dados.
        
        Parameters:
            sequence (Sequence): A sequência a ser adicionada.
        """
        if sequence.id and sequence.description and sequence.seq and sequence.id not in self.database:
            self.database[sequence.id] = sequence

    def get_sequence_by_id(self, id: str) -> Sequence | None:
        """
        Busca uma sequência no banco de dados pelo ID fornecido.
        
        Parameters:
            id (str): O ID da sequência a ser buscada.
        
        Returns:
            Sequence|None: A sequência correspondente ao ID, ou None se não for encontrada.
        """
        if id in self.database:
            return self.database[id]
        else:
            return None

    def load_from_fasta(self, filename: str):
        """
        Carrega sequências de um arquivo FASTA e as adiciona ao banco de dados.
        
        Parameters:
            filename (str): O caminho do arquivo FASTA a ser carregado.
        """
        with open(filename, 'r') as file:
            id = ''
            seq = ''
            for line in file:
                line = line.strip()  # Remove espaços em branco no início e no final
                if line.startswith('>'):
                    if id:
                        self.database[id] = Sequence(id, "No description", seq)
                    id = line[1:]
                    seq = ''
                else:
                    seq += line
            if id:
                self.database[id] = Sequence(id, "No description", seq)  
        
