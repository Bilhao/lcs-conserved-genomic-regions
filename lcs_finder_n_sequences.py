from sequence import Sequence
from itertools import product

class LCSFinderNSequences():
    """
    Classe para encontrar a subsequência comum mais longa (LCS) entre N sequências.

    Attributes:
        sequences (list[Sequence]): Lista de objetos Sequence representando as sequências a serem comparadas.
    """
    def __init__(self, sequences: list[Sequence]):
        self.sequences = sequences

        self.dd = self._initialization()
        self.dd = self._filling(self.dd)
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento do LCS (Longest Common Subsequence) para N sequências.
        
        Utiliza programação dinâmica para preencher um dicionário que armazena os comprimentos
        do LCS para todas as combinações de índices das sequências. O dicionário é inicializado
        com zeros e preenchido iterativamente, considerando se os caracteres atuais das 
        sequências são iguais ou não.

        Returns:
            int: Comprimento do LCS para as N sequências.
        """
        return self.dd[tuple(seq.length() for seq in self.sequences)]
    
    def get_lcs(self) -> str:
        """
        Obtém o LCS (Longest Common Subsequence) para N sequências.
        Utiliza o dicionário preenchido pelo método get_lcs_length para reconstruir o LCS
        a partir dos índices das sequências.

        Returns:
            str: O LCS formado pelas N sequências.
        """
        # Reconstrução do LCS a partir do dicionário
        indices = [seq.length() for seq in self.sequences]
        lcs_chars = []

        while all(i > 0 for i in indices):  # Enquanto todos os índices forem maiores que 0
            chars = [self.sequences[i].seq[indices[i] - 1] for i in range(len(self.sequences))]  # Pega o caractere atual de cada sequência
            if all(c == chars[0] for c in chars):  # Se todos os caracteres são iguais, faz parte do LCS
                lcs_chars.append(chars[0])
                indices = [i - 1 for i in indices]
            else:  # Se não são iguais, retrocede em uma das sequências (aquela que maximiza o valor do LCS)
                max_index = max(range(len(indices)), key=lambda i: self.dd[tuple(indices[:i] + [indices[i] - 1] + indices[i + 1:])] if indices[i] > 0 else -1)
                indices[max_index] -= 1

        # Retorna o LCS invertido (pois foi construído de trás para frente)
        return ''.join(reversed(lcs_chars))

    def _initialization(self):
        """
        Inicializa um dicionário dinâmico (dd) para o cálculo do LCS de N sequências.

        Cria um dicionário onde as chaves são tuplas de índices (uma posição para cada sequência)
        e os valores são inicialmente 0. Cada tupla representa um estado possível do alinhamento
        (quantos caracteres já foram considerados de cada sequência).

        Exemplo para 4 sequências de tamanho 3:
        As chaves serão (0,0,0,0), (0,0,0,1), ..., (3,3,3,3), todas iniciadas com valor 0.
        """
        lengths = [seq.length() for seq in self.sequences]
        n = len(self.sequences)
        dd = {}

        def fill(indices):
            """
            Função recursiva para preencher o dicionário dinâmico com todas as combinações de índices.
            """
            if len(indices) == n:  # Se já temos índices para todas as sequências
                dd[tuple(indices)] = 0  # Inicializa o valor como 0
                return
            for i in range(lengths[len(indices)] + 1):  # De 0 até o comprimento da sequência
                fill(indices + [i])

        fill([])
        return dd

    def _filling(self, dd) -> dict:
        """
        Preenche o dicionário dinâmico (dd) com os valores do LCS para todas as combinações de índices.

        Para cada combinação de índices (um para cada sequência), verifica:
        - Se todos os caracteres nas posições atuais das sequências são iguais:
            - Soma 1 ao valor do estado anterior (todos os índices -1).
        - Caso contrário:
            - Considera todas as possibilidades de "andar para trás" em apenas uma das sequências,
              pega o maior valor entre elas e atribui ao estado atual.

        No final, dd[tuple(comprimento de cada sequência)] terá o comprimento do LCS para todas.

        Parameters:
            dd (dict): Dicionário dinâmico inicializado com zeros, onde as chaves são tuplas de índices.

        Returns:
            dict: Dicionário preenchido com os comprimentos do LCS para todas as combinações de índices.
        """
        lengths = [seq.length() for seq in self.sequences]
        n = len(self.sequences)

        # Gera todas as combinações possíveis de índices (excluindo o índice 0)
        for indices in product(*[range(1, l + 1) for l in lengths]):  # product gera todas as combinações de índices possíveis usando o produto cartesiano. Ex: product((0,1), (0,1), (0,1)) --> (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0) ...
            # Pega o caractere atual de cada sequência
            chars = [self.sequences[i].seq[indices[i] - 1] for i in range(n)] 

            if all(c == chars[0] for c in chars):  # Se todos os caracteres são iguais, soma 1 ao valor do estado anterior
                prev_indices = tuple(idx - 1 for idx in indices)
                dd[indices] = dd[prev_indices] + 1
            else:
                # Se não são iguais, tenta "andar para trás" em cada sequência individualmente
                max_val = 0
                for i in range(n):
                    reduced_indices = list(indices)
                    reduced_indices[i] -= 1
                    # Só considera se o índice não ficou negativo
                    if reduced_indices[i] >= 0:
                        max_val = max(max_val, dd[tuple(reduced_indices)])
                dd[indices] = max_val
        return dd

