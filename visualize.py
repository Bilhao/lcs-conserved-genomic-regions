from sequence import Sequence
from sequence_database import SequenceDatabase
from sequence_alignment import SequenceAlignment
from lcs_finder import LCSFinder
from lcs_finder_n_sequences import LCSFinderNSequences
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Visualize:
    def __init__(self, sequence_db: SequenceDatabase):
        self.sequence_db = sequence_db

        if len(self.sequence_db.database.values()) > 3:
            self.lcs_finder = LCSFinderNSequences(list(self.sequence_db.database.values()))
        else:
            self.lcs_finder = LCSFinder(
                list(self.sequence_db.database.values())[0],
                list(self.sequence_db.database.values())[1],
                list(self.sequence_db.database.values())[2] if len(self.sequence_db.database.values()) > 2 else None
            )
        self.alignment = self.lcs_finder.compute_lcs()


    def visualize_sequences(self):
        """
        Visualiza o LCS e o alinhamento das sequências usando Plotly.
        Esta função cria um gráfico de calor (heatmap) para representar o alinhamento das sequências de DNA.
        """
        ids = list(self.sequence_db.database.keys())

        # Prepara as sequências alinhadas para visualização.
        # Inclui as duas primeiras sequências e a terceira, se existir.
        aligned_seqs = [self.alignment.aligned_seq1, self.alignment.aligned_seq2]
        if self.alignment.aligned_seq3:
            aligned_seqs.append(self.alignment.aligned_seq3)

        all_chars = set()
        for seq_str in aligned_seqs:
            all_chars.update(list(seq_str))

        sorted_unique_chars = sorted(list(all_chars))
        char_to_int_idx = {char: i for i, char in enumerate(sorted_unique_chars)}

        # Constrói a matriz 'z' (valores numéricos para o heatmap) e a matriz de texto para exibição.
        z_sequences_indexed = []  # Armazena os índices dos caracteres para o heatmap.
        text_sequences = []  # Armazena os caracteres dos nucleotídeos para exibição no heatmap.
        for seq_str in aligned_seqs:
            # Converte cada caractere da sequência para seu índice correspondente.
            row = [char_to_int_idx.get(char, -1) for char in seq_str] # Usar -1 ou algum valor para chars inesperados se necessário
            z_sequences_indexed.append(row)
            # Adiciona a sequência original (como lista de caracteres) para o texto do heatmap.
            text_sequences.append(list(seq_str))

        # Obtém o comprimento do alinhamento (todas as sequências alinhadas têm o mesmo comprimento).
        alignment_length = len(aligned_seqs[0])
        # Cria uma lista de posições para o eixo x do gráfico.
        positions_for_plot_dna = list(range(alignment_length))

        # Cria a figura do Plotly com um heatmap.
        fig = go.Figure(data=go.Heatmap(
            z=z_sequences_indexed,  # Dados numéricos para as cores do heatmap.
            x=positions_for_plot_dna,  # Posições no alinhamento (eixo x).
            y=ids,  # IDs das sequências (eixo y).
            text=text_sequences,  # Texto a ser exibido em cada célula (nucleotídeos).
            texttemplate="%{text}",  # Formato para exibir o texto.
            colorscale="Turbo",  # Escala de cores definida anteriormente.
            showscale=False,  # Oculta a barra de escala de cores.
            xgap=1,  # Espaçamento entre células no eixo x.
            ygap=1,  # Espaçamento entre células no eixo y.
            hovertemplate="ID: %{y}<br>Pos: %{x}<br>Base: %{text}<extra></extra>" # Informação exibida ao passar o mouse.
        ))

        # Configura o layout da figura.
        fig.update_layout(
            title_text="Visualização ilustrando as subsequências conservadas identificadas",
            height=max(400, 200 + len(ids) * 30), # Altura dinâmica baseada no número de sequências.
            margin=dict(l=120, r=50, t=100, b=50), # Margens do gráfico.
        )

        # Configura os ticks do eixo x.
        x_tickvals_dna = list(range(alignment_length)) # Valores dos ticks.
        x_ticktext_dna = [str(i + 1) for i in x_tickvals_dna] # Texto dos ticks (posições começando de 1).

        fig.update_xaxes(
            showticklabels=True,
            tickvals=x_tickvals_dna,
            ticktext=x_ticktext_dna,
            title_text="Posição no Alinhamento",
            rangeslider_visible=True,
            # Define o intervalo inicial visível do seletor de intervalo (máximo de 50 posições).
            range=[-0.5, alignment_length - 0.5 if alignment_length < 50 else 49.5]
        )

        fig.update_yaxes(
            autorange="reversed",  # Inverte a ordem do eixo y para exibir a primeira sequência no topo.
            title_text="ID da Sequência"
        )
        
        fig.show(renderer="browser")