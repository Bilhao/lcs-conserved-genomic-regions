from sequence import Sequence
from sequence_alignment import SequenceAlignment
import plotly.express as px
import numpy as np


class LCSFinder():
    """
    Classe para encontrar a maior subsequência comum (LCS) entre duas ou três sequências.
    Esta classe utiliza programação dinâmica para calcular o LCS e reconstruir as sequências alinhadas.
    
    Attributes:
        seq1 (Sequence): A primeira sequência a ser comparada.
        seq2 (Sequence): A segunda sequência a ser comparada.
        seq3 (Sequence, optional): A terceira sequência a ser comparada. Se não for fornecida, o LCS será calculado apenas entre seq1 e seq2.
    """
    def __init__(self, seq1: Sequence, seq2: Sequence, seq3: Sequence = None):
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        
        self.matrix = self._dynamic_matrix_initialization()  # Inicializa a matriz dinâmica ou tensor
        self.matrix = self._dynamic_matrix_filled(self.matrix)  # Preenche a matriz dinâmica ou tensor
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        lcs = self._lcs_reconstruction(self.matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)  # Alinha as sequencias 
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, len(lcs), self.seq3, aligned3 if self.seq3 else None)
        
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento da maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            int: O comprimento do LCS.
        """
        if self.seq3 is None:
            return self.matrix[-1][-1]
        else:
            return self.matrix[-1][-1][-1]

    def get_lcs(self) -> str:
        """
        Obtém a maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            str: A LCS reconstruída a partir da matriz dinâmica ou tensor preenchido.
        """
        lcs = self._lcs_reconstruction(self.matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        return lcs  # Retorna a LCS reconstruída a partir da matriz dinâmica ou tensor preenchido

    def visualize(self):
        """
        Visualiza o LCS e o alinhamento das sequências usando Plotly.
        Esta função cria um gráfico interativo que mostra a matriz de LCS e as setas indicando o alinhamento das sequências.
        """
        np_matrix = np.array(self.matrix)  # Converte a matriz para um array NumPy

        if self.seq3 is None:
            fig = px.imshow(
                np_matrix.T,  # Transposta para alinhar corretamente as sequências
                title='LCS - 2 Sequences',
                labels=dict(x="Sequence 1", y="Sequence 2", color="LCS Value"),
                text_auto=True,
            )
            fig.update_layout(
                xaxis=dict(tickmode='array', tickvals=list(range(self.seq1.length() + 1)), ticktext=['0'] + list(self.seq1.seq)),
                yaxis=dict(tickmode='array', tickvals=list(range(self.seq2.length() + 1)), ticktext=['0'] + list(self.seq2.seq)),
            )
            fig.update_xaxes(side="top")
            fig.update_yaxes(autorange="reversed")

            i, j = self.seq1.length(), self.seq2.length()
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                    fig.add_shape(
                        type="rect",
                        x0=i - 0.5, x1=i + 0.5,
                        y0=j - 0.5, y1=j + 0.5,
                        line=dict(color="black", width=2),
                        layer="above"
                    )
                    fig.add_annotation(
                        x=i,
                        y=j,
                        ax=i - 1,
                        ay=j - 1,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowwidth=2,
                        arrowhead=5,
                        arrowside="start",
                        arrowcolor="red",
                    )
                    i -= 1
                    j -= 1
                elif self.matrix[i-1][j] >= self.matrix[i][j-1]:
                    fig.add_annotation(
                        x=i,
                        y=j,
                        ax=i - 1,
                        ay=j,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowwidth=2,
                        arrowhead=5,
                        arrowside="start",
                        arrowcolor="red",
                    )
                    i -= 1
                else:
                    fig.add_annotation(
                        x=i,
                        y=j,
                        ax=i,
                        ay=j - 1,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowwidth=2,
                        arrowhead=5,
                        arrowside="start",
                        arrowcolor="red",
                    )
                    j -= 1
            fig.show(renderer="browser")  # Exibe o gráfico no navegador
        else:
            ...

    def _dynamic_matrix_initialization(self) -> list[list[int]] | list[list[list[int]]]:
        """
        Inicializa a matriz dinâmica ou tensor para armazenar os valores de LCS.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor inicializado com zeros.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 1. Inicialização da matriz dinâmica (todos os valores iguais a 0 e tamanho (n+1) x (m+1):
        if self.seq3 is None:
            return [[0 for _ in range(m+1)] for _ in range(n+1)]
        else:
            return [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]

    def _dynamic_matrix_filled(self, matrix: list[list[int]] | list[list[list[int]]]) -> list[list[int]] | list[list[list[int]]]:
        """
        Preenche a matriz dinâmica ou tensor com os valores de LCS usando programação dinâmica.
        
        Parameters:
            matrix (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor inicializado com zeros.
        
        Returns:
            list[list[int]] | list[list[list[int]]]: A matriz dinâmica ou tensor preenchido com os valores de LCS.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0
        
        # 2. Preenchimento da matriz ou tensor
        if self.seq3 is None:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                        matrix[i][j] = matrix[i-1][j-1] + 1
                    else:
                        matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1])
        else:
            for i in range(1, n+1):
                for j in range(1, m+1):
                    for w in range(1, k+1):
                        if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(w-1):
                            matrix[i][j][w] = matrix[i-1][j-1][w-1] + 1
                        else:
                            matrix[i][j][w] = max(matrix[i-1][j][w], matrix[i][j-1][w], matrix[i][j][w-1])
        return matrix  # Retorna a matriz preenchida ou o tensor preenchido
    
    def _lcs_reconstruction(self, matrix) -> str:
        """
        Reconstrói a subsequência comum mais longa (LCS) a partir da matriz dinâmica ou tensor preenchido.
        
        Parameters:
            matrix (list[list[int]] | list[list[list[int]]]): A matriz dinâmica ou tensor preenchido com os valores de LCS.
        
        Returns:
            str: A subsequência comum mais longa (LCS) reconstruída a partir da matriz dinâmica ou tensor preenchido.
        """
        lcs = "" 
        i = self.seq1.length()
        j = self.seq2.length()
        k = self.seq3.length() if self.seq3 else 0

        # 3. Reconstrução da subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        if not self.seq3:
            while i > 0 and j > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                else:
                    if matrix[i-1][j] >= matrix[i][j-1]:  # Se o valor de cima for maior ou igual, ir para o valor de cima
                        i -= 1 
                    else:  # Caso contrário, ir para o valor da esquerda
                        j -= 1
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, no caso foi escolhido ir para cima
            return lcs
        else:
            while i > 0 and j > 0 and k > 0:
                if self.seq1.char_at(i-1) == self.seq2.char_at(j-1) == self.seq3.char_at(k-1):
                    lcs = self.seq1.char_at(i-1) + lcs
                    i -= 1
                    j -= 1
                    k -= 1
                else:
                    # Decide de qual direção está o maior valor no tensor
                    if matrix[i-1][j][k] >= matrix[i][j-1][k] and matrix[i-1][j][k] >= matrix[i][j][k-1]:
                        i -= 1  # Ir para cima
                    elif matrix[i][j-1][k] >= matrix[i-1][j][k] and matrix[i][j-1][k] >= matrix[i][j][k-1]:
                        j -= 1  # Ir para esquerda
                    else:
                        k -= 1  # Ir para frente
                    # OBS: Se os valores forem iguais, pode-se ir tanto para a cima, tanto para a esquerda, tanto para frente.
            return lcs

    def _sequence_alignment(self, lcs: str) -> tuple[str, str, str]:
        """
        Alinha as sequências com base na subsequência comum mais longa (LCS) reconstruída.
        
        Parameters:
            lcs (str): A subsequência comum mais longa (LCS) reconstruída a partir da matriz dinâmica ou tensor preenchido.
        
        Returns:
            tuple[str, str, str]: As sequências alinhadas (seq1, seq2, seq3) com base na LCS.
        """
        n = self.seq1.length()
        m = self.seq2.length()
        w = self.seq3.length() if self.seq3 else 0

        # Alinhamento das sequências       
        aligned1, aligned2, aligned3= "", "", ""  # Variáveis para armazenar os alinhamentos
        i, j, k = 0, 0, 0  # Índices para percorrer as sequências 
        l = 0  # Índice para percorrer a LCS
        if not self.seq3:
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:  # Se o caractere da seq1 não for igual ao caractere da LCS, adiciona traços
                    aligned1 += self.seq1.char_at(i)
                    aligned2 += "-"
                    i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:  # Se o caractere da seq2 não for igual ao caractere da LCS, adiciona traços
                    aligned1 += "-"
                    aligned2 += self.seq2.char_at(j)
                    j += 1
                aligned1 += self.seq1.char_at(i)  # Adiciona o caractere da LCS
                aligned2 += self.seq2.char_at(j)
                i += 1
                j += 1
                l += 1
            aligned1 += self.seq1.seq[i:] # Adiciona o restante da sequência seq1
            aligned2 += self.seq2.seq[j:] # Adiciona o restante da sequência seq2
            if len(aligned1) < len(aligned2):
                aligned1 += "-" * (len(aligned2) - len(aligned1))  # Preenche com traços se necessário
            if len(aligned2) < len(aligned1):
                aligned2 += "-" * (len(aligned1) - len(aligned2))

        else: 
            while l < len(lcs):
                while i < n and self.seq1.char_at(i) != lcs[l]:
                    if self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    else: 
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += "-"
                        i += 1
                while j < m and self.seq2.char_at(j) != lcs[l]:
                    if self.seq2.char_at(j) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    elif self.seq2.char_at(j) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) == self.seq3.char_at(k) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    else:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        j += 1
                while k < w and self.seq3.char_at(k) != lcs[l]:
                    if self.seq3.char_at(k) == self.seq1.char_at(i) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        i += 1
                        k += 1
                    elif self.seq3.char_at(k) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += "-"
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += self.seq3.char_at(k)
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) == self.seq2.char_at(j) != lcs[l]:
                        aligned1 += self.seq1.char_at(i)
                        aligned2 += self.seq2.char_at(j)
                        aligned3 += "-"
                        i += 1
                        j += 1
                    else:
                        aligned1 += "-"
                        aligned2 += "-"
                        aligned3 += self.seq3.char_at(k)
                        k += 1
                aligned1 += self.seq1.char_at(i)
                aligned2 += self.seq2.char_at(j)
                aligned3 += self.seq3.char_at(k)
                i += 1
                j += 1
                k += 1
                l += 1

            aligned1 += self.seq1.seq[i:] # Adiciona o restante da sequência seq1
            aligned2 += self.seq2.seq[j:] # Adiciona o restante da sequência seq2
            aligned3 += self.seq3.seq[k:] # Adiciona o restante da sequência seq3

            max_lenght = max(len(aligned1), len(aligned2), len(aligned3))
            min_lenght = min(len(aligned1), len(aligned2), len(aligned3))

            while min_lenght < max_lenght:
                if len(aligned1) < max_lenght:
                    if i == n or j == m or k == w:
                        aligned1 += "-" * (max_lenght - len(aligned1))
                    elif self.seq1.char_at(i) != self.seq2.char_at(j) and self.seq2.char_at(j) == self.seq3.char_at(k):
                        aligned1 = aligned1[:i] + "-" + aligned1[i:]
                        j += 1
                        k += 1
                    elif self.seq1.char_at(i) != self.seq2.char_at(j) and self.seq1.char_at(i) == self.seq3.char_at(k):
                        aligned1 = aligned1[:i+1] + "-" + aligned1[i+1:]
                        j += 1
                        k += 1
                if len(aligned2) < max_lenght:
                    if i == n or j == m or k == w:
                        aligned2 += "-" * (max_lenght - len(aligned2))
                    elif self.seq2.char_at(j) != self.seq1.char_at(i) and self.seq1.char_at(i) == self.seq3.char_at(k):
                        aligned2 = aligned2[:j] + "-" + aligned2[j:]
                        i += 1
                        k += 1
                    elif self.seq2.char_at(j) != self.seq1.char_at(i) and self.seq2.char_at(j) == self.seq3.char_at(k):
                        aligned2 = aligned2[:j+1] + "-" + aligned2[j+1:]
                        i += 1
                        k += 1
                if len(aligned3) < max_lenght:
                    if i == n or j == m or k == w:
                        aligned3 += "-" * (max_lenght - len(aligned3))
                    elif self.seq3.char_at(k) != self.seq1.char_at(i) and self.seq1.char_at(i) == self.seq2.char_at(j):
                        aligned3 = aligned3[:k] + "-" + aligned3[k:]
                        i += 1
                        j += 1
                    elif self.seq3.char_at(k) != self.seq1.char_at(i) and self.seq3.char_at(k) == self.seq2.char_at(j):
                        aligned3 = aligned3[:k+1] + "-" + aligned3[k+1:]
                        i += 1
                        j += 1
                max_lenght = max(len(aligned1), len(aligned2), len(aligned3))
                min_lenght = min(len(aligned1), len(aligned2), len(aligned3))
                
        return aligned1, aligned2, aligned3