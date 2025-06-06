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
    
    def compute_lcs(self) -> SequenceAlignment:
        """
        Computa o alinhamento de duas ou três sequências, retornando um objeto SequenceAlignment.

        Returns:
            SequenceAlignment: Um objeto que contém informações relevantes da sequência.
        """
        matrix = self._dynamic_matrix_initialization()  # Inicializa a matriz dinâmica ou tensor
        matrix = self._dynamic_matrix_filled(matrix)  # Preenche a matriz dinâmica ou tensor
        lcs = self._lcs_reconstruction(matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)  # Alinha as sequencias 
        
        return SequenceAlignment(self.seq1, self.seq2, aligned1, aligned2, len(lcs), self.seq3, aligned3 if self.seq3 else None)
        
    
    def get_lcs_length(self) -> int:
        """
        Calcula o comprimento da maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            int: O comprimento do LCS.
        """                
        matrix = self._dynamic_matrix_initialization()  # Inicializa a matriz dinâmica ou tensor
        matrix = self._dynamic_matrix_filled(matrix)  # Preenche a matriz dinâmica ou tensor
    
        return matrix[-1][-1] if self.seq3 is None else matrix[-1][-1][-1]  # Retorna o comprimento do LCS (último elemento da matriz/tensor)

    def get_lcs(self) -> str:
        """
        Obtém a maior subsequência comum (LCS) entre duas ou três sequências.

        Returns:
            str: A LCS reconstruída a partir da matriz dinâmica ou tensor preenchido.
        """
        matrix = self._dynamic_matrix_initialization()
        matrix = self._dynamic_matrix_filled(matrix)  # Preenche a matriz dinâmica ou tensor
        lcs = self._lcs_reconstruction(matrix)  # Reconstrói a subsequência comum mais longa (LCS) usando a matriz dinâmica ou tensor preenchido
        return lcs  # Retorna a LCS reconstruída a partir da matriz dinâmica ou tensor preenchido

    def visualize(self):
        """
        Visualiza o LCS e o alinhamento das sequências usando Plotly.
        Esta função cria um gráfico interativo que mostra a matriz de LCS e as setas indicando o alinhamento das sequências.
        """
        matrix = self._dynamic_matrix_initialization()
        matrix = self._dynamic_matrix_filled(matrix)
        lcs = self._lcs_reconstruction(matrix)  # Obtém o comprimento do LCS
        aligned1, aligned2, aligned3 = self._sequence_alignment(lcs)
        
        np_matrix = np.array(matrix)  # Converte a matriz para um array NumPy

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
                elif matrix[i-1][j] >= matrix[i][j-1]:
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

            alignment_text = (
                f"Aligned Sequence 1: {aligned1}<br>"
                f"Aligned Sequence 2: {aligned2}<br>"
                f"Conserved subsequence: {lcs}<br>"
                f"LCS Length: {len(lcs)}<br>"
            )
            # Adiciona a anotação do lado direito do gráfico, alinhamento dinâmico
            fig.add_annotation(
                text=alignment_text,
                xref="paper", yref="paper",
                x=0.9, y=0.5,
                showarrow=False,
                font=dict(size=13),
                xanchor="auto",
                yanchor="middle",
            )
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
        # Imperativa:
        if self.seq3 is None:
            r1 = []
            i = 0
            while i < n + 1:
                r2 = []
                j = 0
                while j < m + 1:
                    r2.append(0) 
                    j += 1
                r1.append(r2)
                i += 1
            return r1
        else:
            r1 = []
            i = 0
            while i < n + 1:
                r2 = []
                j = 0
                while j < m + 1:
                    r3 = []
                    w = 0
                    while w < k + 1:
                        r3.append(0)
                        w += 1
                    r2.append(r3) 
                    j += 1
                r1.append(r2)
                i += 1
            return r1
        # Funcional:
        """
        if self.seq3 is None:
            return [[0 for _ in range(m+1)] for _ in range(n+1)]
        else:
            return [[[0 for _ in range(k+1)] for _ in range(m+1)] for _ in range(n+1)]
        """

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
            # 2. Lógica: Índices dos caracteres da LCS ("ATTG") em cada sequência.
            # Esta é a informação central que guia o alinhamento.
            indices1 = [0, 1, 4, 5]  # Índices de 'A', 'T', 'T', 'G' em s1
            indices2 = [0, 1, 4, 6]  # Índices de 'A', 'T', 'T', 'G' em s2
            indices3 = [0, 2, 3, 6]  # Índices de 'A', 'T', 'T', 'G' em s3

            alinhada1, alinhada2, alinhada3 = "", "", ""
            p1, p2, p3 = 0, 0, 0

            # 3. Processo de alinhamento
            # Itera sobre cada caractere da LCS para criar os blocos de alinhamento
            for i in range(len(lcs)):
                lcs_char = lcs[i]

                # Pega a posição do próximo caractere da LCS em cada sequência
                prox_p1 = indices1[i]
                prox_p2 = indices2[i]
                prox_p3 = indices3[i]

                # Extrai os "segmentos" entre o caractere da LCS anterior e o atual
                seg1 = self.seq1.seq[p1:prox_p1]
                seg2 = self.seq2.seq[p2:prox_p2]
                seg3 = self.seq3.seq[p3:prox_p3]

                # Determina o comprimento máximo entre os segmentos para inserir os gaps
                max_len = max(len(seg1), len(seg2), len(seg3))

                # Adiciona os segmentos às sequências alinhadas, preenchendo com '-'
                alinhada1 += seg1.ljust(max_len, '-')
                alinhada2 += seg2.ljust(max_len, '-')
                alinhada3 += seg3.ljust(max_len, '-')

                # Adiciona o caractere da LCS, que agora está alinhado
                alinhada1 += lcs_char
                alinhada2 += lcs_char
                alinhada3 += lcs_char

                # Atualiza os ponteiros para a posição logo após o caractere da LCS
                p1 = prox_p1 + 1
                p2 = prox_p2 + 1
                p3 = prox_p3 + 1

            # Adiciona os caracteres restantes (a "cauda") de cada sequência
            cauda1 = self.seq1.seq[p1:]
            cauda2 = self.seq2.seq[p2:]
            cauda3 = self.seq3.seq[p3:]

            # Preenche a cauda para que todas as sequências terminem com o mesmo comprimento
            max_cauda_len = max(len(cauda1), len(cauda2), len(cauda3))
            alinhada1 += cauda1.ljust(max_cauda_len, '-')
            alinhada2 += cauda2.ljust(max_cauda_len, '-')
            alinhada3 += cauda3.ljust(max_cauda_len, '-')
            
                
        return alinhada1, alinhada2, alinhada3

    