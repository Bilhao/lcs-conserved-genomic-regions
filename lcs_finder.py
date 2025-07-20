from sequence import Sequence
from sequence_alignment import SequenceAlignment


class LCSFinder():
    """
    Classe para alinhar sequências usando o algoritmo Needleman-Wunsch.
    Esta classe utiliza programação dinâmica para calcular o alinhamento global ótimo 
    entre duas ou três sequências com base em scores de match, mismatch e gap.
    
    Attributes:
        seq1 (Sequence): A primeira sequência a ser comparada.
        seq2 (Sequence): A segunda sequência a ser comparada.
        seq3 (Sequence, optional): A terceira sequência a ser comparada. Se não for fornecida, o alinhamento será calculado apenas entre seq1 e seq2.
        match_score (int): Score para match entre caracteres idênticos (padrão: 2).
        mismatch_penalty (int): Penalidade para mismatch entre caracteres diferentes (padrão: -1).
        gap_penalty (int): Penalidade para inserção de gaps (padrão: -1).
    """
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None, 
                 match_score: int = 2, mismatch_penalty: int = -1, gap_penalty: int = -1):
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        self.match_score = match_score
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
        
        self.dp = self._initialization()  # Inicializa a matriz dinâmica ou tensor
        self.dp = self._filling(self.dp)  # Preenche a matriz dinâmica ou tensor
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento global ótimo de duas ou três sequências usando Needleman-Wunsch, 
        retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes do alinhamento.
        """
        aligned1, aligned2, aligned3 = self._needleman_wunsch_traceback(self.dp)  # Reconstrói o alinhamento ótimo
        
        # Calcula o número de matches para o score
        if self.seq3 is None:
            matches = self._count_matches(aligned1, aligned2, None)
        else:
            matches = self._count_matches(aligned1, aligned2, aligned3)
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, matches, self.seq3, aligned3 if self.seq3 else None)
        
    
    def get_lcs_length(self) -> int:
        """
        Retorna o score do alinhamento ótimo entre duas ou três sequências.

        Returns:
            int: O score do alinhamento ótimo.
        """
        if self.seq3 is None:
            return self.dp[-1][-1]
        else:
            return self.dp[-1][-1][-1]

    def get_lcs(self) -> str:
        """
        Retorna a representação do alinhamento ótimo como string.
        Para compatibilidade com a interface existente.

        Returns:
            str: Uma representação simplificada do alinhamento.
        """
        aligned1, aligned2, aligned3 = self._needleman_wunsch_traceback(self.dp)
        
        # Retorna a primeira sequência alinhada como representação do "LCS"
        # Isso mantém compatibilidade com o código existente
        return aligned1.replace('-', '')

    def _initialization(self) -> list[list[int]] | list[list[list[int]]]:
        """
        Inicializa a matriz dinâmica ou tensor para armazenar os scores do alinhamento.
        Para Needleman-Wunsch, a primeira linha e coluna são inicializadas com penalidades de gap.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor inicializado.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        if self.seq3 is None:
            # Inicialização da matriz dinâmica 2D para Needleman-Wunsch
            dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
            
            # Inicializa primeira linha (gaps na primeira sequência)
            for j in range(1, m+1):
                dp[0][j] = dp[0][j-1] + self.gap_penalty
                
            # Inicializa primeira coluna (gaps na segunda sequência)
            for i in range(1, n+1):
                dp[i][0] = dp[i-1][0] + self.gap_penalty
                
            return dp
        else:
            # Inicialização do tensor 3D para três sequências
            dp = [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]
            
            # Inicializa as faces do tensor com penalidades de gap
            for i in range(1, n+1):
                dp[i][0][0] = dp[i-1][0][0] + self.gap_penalty
            for j in range(1, m+1):
                dp[0][j][0] = dp[0][j-1][0] + self.gap_penalty
            for w in range(1, k+1):
                dp[0][0][w] = dp[0][0][w-1] + self.gap_penalty
                
            # Inicializa as arestas do tensor
            for i in range(1, n+1):
                for j in range(1, m+1):
                    dp[i][j][0] = max(
                        dp[i-1][j][0] + self.gap_penalty,
                        dp[i][j-1][0] + self.gap_penalty,
                        dp[i-1][j-1][0] + (self.match_score if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) else self.mismatch_penalty)
                    )
                    
            for i in range(1, n+1):
                for w in range(1, k+1):
                    dp[i][0][w] = max(
                        dp[i-1][0][w] + self.gap_penalty,
                        dp[i][0][w-1] + self.gap_penalty,
                        dp[i-1][0][w-1] + (self.match_score if self.seq1.char_at(i-1) == self.seq3.char_at(w-1) else self.mismatch_penalty)
                    )
                    
            for j in range(1, m+1):
                for w in range(1, k+1):
                    dp[0][j][w] = max(
                        dp[0][j-1][w] + self.gap_penalty,
                        dp[0][j][w-1] + self.gap_penalty,
                        dp[0][j-1][w-1] + (self.match_score if self.seq2.char_at(j-1) == self.seq3.char_at(w-1) else self.mismatch_penalty)
                    )
                    
            return dp

    def _filling(self, dp: list[list[int]] | list[list[list[int]]]) -> list[list[int]] | list[list[list[int]]]:
        """
        Preenche a matriz dinâmica ou tensor com os scores usando o algoritmo Needleman-Wunsch.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor inicializado.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor preenchido com os scores.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0
        
        if self.seq3 is None:
            # Preenchimento da matriz 2D para duas sequências
            for i in range(1, n+1):
                for j in range(1, m+1):
                    # Score para match/mismatch
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        match_score = dp[i-1][j-1] + self.match_score
                    else:
                        match_score = dp[i-1][j-1] + self.mismatch_penalty
                    
                    # Score para gap na primeira sequência
                    gap1_score = dp[i-1][j] + self.gap_penalty
                    
                    # Score para gap na segunda sequência
                    gap2_score = dp[i][j-1] + self.gap_penalty
                    
                    # Escolhe o melhor score
                    dp[i][j] = max(match_score, gap1_score, gap2_score)
        else:
            # Preenchimento do tensor 3D para três sequências
            for i in range(1, n+1):
                for j in range(1, m+1):
                    for w in range(1, k+1):
                        scores = []
                        
                        # Match/mismatch entre todas as três sequências
                        if (self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1)):
                            scores.append(dp[i-1][j-1][w-1] + self.match_score)
                        else:
                            scores.append(dp[i-1][j-1][w-1] + self.mismatch_penalty)
                        
                        # Gaps em diferentes combinações
                        scores.append(dp[i-1][j][w] + self.gap_penalty)      # Gap na seq1
                        scores.append(dp[i][j-1][w] + self.gap_penalty)      # Gap na seq2
                        scores.append(dp[i][j][w-1] + self.gap_penalty)      # Gap na seq3
                        scores.append(dp[i-1][j-1][w] + self.gap_penalty)    # Gap na seq3, match seq1-seq2
                        scores.append(dp[i-1][j][w-1] + self.gap_penalty)    # Gap na seq2, match seq1-seq3
                        scores.append(dp[i][j-1][w-1] + self.gap_penalty)    # Gap na seq1, match seq2-seq3
                        
                        dp[i][j][w] = max(scores)
        
        return dp
    
    def _needleman_wunsch_traceback(self, dp) -> tuple[str, str, str]:
        """
        Reconstrói o alinhamento ótimo através de traceback da matriz/tensor de scores.
        
        Parameters:
            dp (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor preenchido com os scores.
        
        Returns:
            tuple[str, str, str]: As sequências alinhadas (seq1, seq2, seq3).
        """
        aligned1, aligned2, aligned3 = "", "", ""
        i = self.seq1.length()
        j = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        if self.seq3 is None:
            # Traceback para duas sequências
            while i > 0 or j > 0:
                if i > 0 and j > 0:
                    # Calcular scores para determinar o caminho
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        diagonal_score = dp[i-1][j-1] + self.match_score
                    else:
                        diagonal_score = dp[i-1][j-1] + self.mismatch_penalty
                    
                    up_score = dp[i-1][j] + self.gap_penalty if i > 0 else float('-inf')
                    left_score = dp[i][j-1] + self.gap_penalty if j > 0 else float('-inf')
                    
                    # Escolher o caminho que gerou o score atual
                    if dp[i][j] == diagonal_score:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        i -= 1
                        j -= 1
                    elif dp[i][j] == up_score:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        i -= 1
                    else:  # left_score
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        j -= 1
                elif i > 0:
                    # Só restam caracteres da primeira sequência
                    aligned1 = self.seq1.char_at(i-1) + aligned1
                    aligned2 = "-" + aligned2
                    i -= 1
                else:  # j > 0
                    # Só restam caracteres da segunda sequência
                    aligned1 = "-" + aligned1
                    aligned2 = self.seq2.char_at(j-1) + aligned2
                    j -= 1
        else:
            # Traceback para três sequências (implementação simplificada)
            while i > 0 or j > 0 or k > 0:
                if i > 0 and j > 0 and k > 0:
                    # Verificar se veio de uma correspondência tripla
                    if (self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(k-1)):
                        diagonal_score = dp[i-1][j-1][k-1] + self.match_score
                    else:
                        diagonal_score = dp[i-1][j-1][k-1] + self.mismatch_penalty
                    
                    if dp[i][j][k] == diagonal_score:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = self.seq3.char_at(k-1) + aligned3
                        i -= 1
                        j -= 1
                        k -= 1
                    elif i > 0 and dp[i][j][k] == dp[i-1][j][k] + self.gap_penalty:
                        aligned1 = self.seq1.char_at(i-1) + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = "-" + aligned3
                        i -= 1
                    elif j > 0 and dp[i][j][k] == dp[i][j-1][k] + self.gap_penalty:
                        aligned1 = "-" + aligned1
                        aligned2 = self.seq2.char_at(j-1) + aligned2
                        aligned3 = "-" + aligned3
                        j -= 1
                    elif k > 0 and dp[i][j][k] == dp[i][j][k-1] + self.gap_penalty:
                        aligned1 = "-" + aligned1
                        aligned2 = "-" + aligned2
                        aligned3 = self.seq3.char_at(k-1) + aligned3
                        k -= 1
                    else:
                        # Fallback: gap na primeira sequência
                        if i > 0:
                            aligned1 = self.seq1.char_at(i-1) + aligned1
                            aligned2 = "-" + aligned2
                            aligned3 = "-" + aligned3
                            i -= 1
                        elif j > 0:
                            aligned1 = "-" + aligned1
                            aligned2 = self.seq2.char_at(j-1) + aligned2
                            aligned3 = "-" + aligned3
                            j -= 1
                        else:
                            aligned1 = "-" + aligned1
                            aligned2 = "-" + aligned2
                            aligned3 = self.seq3.char_at(k-1) + aligned3
                            k -= 1
                elif i > 0:
                    aligned1 = self.seq1.char_at(i-1) + aligned1
                    aligned2 = "-" + aligned2
                    aligned3 = "-" + aligned3
                    i -= 1
                elif j > 0:
                    aligned1 = "-" + aligned1
                    aligned2 = self.seq2.char_at(j-1) + aligned2
                    aligned3 = "-" + aligned3
                    j -= 1
                elif k > 0:
                    aligned1 = "-" + aligned1
                    aligned2 = "-" + aligned2
                    aligned3 = self.seq3.char_at(k-1) + aligned3
                    k -= 1
        
        return aligned1, aligned2, aligned3

    def _count_matches(self, aligned1: str, aligned2: str, aligned3: str = None) -> int:
        """
        Conta o número de posições onde há match exato entre as sequências alinhadas.
        
        Parameters:
            aligned1 (str): Primeira sequência alinhada.
            aligned2 (str): Segunda sequência alinhada.
            aligned3 (str, optional): Terceira sequência alinhada.
        
        Returns:
            int: Número de matches exatos.
        """
        matches = 0
        if aligned3 is None:
            for a, b in zip(aligned1, aligned2):
                if a == b and a != '-':
                    matches += 1
        else:
            for a, b, c in zip(aligned1, aligned2, aligned3):
                if a == b == c and a != '-':
                    matches += 1
        return matches