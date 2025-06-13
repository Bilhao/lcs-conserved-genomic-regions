from sequence import Sequence
from sequence_database import SequenceDatabase
from sequence_alignment import SequenceAlignment
from lcs_finder import LCSFinder
from lcs_finder_n_sequences import LCSFinderNSequences
import plotly.graph_objects as go

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
        self.alignment: SequenceAlignment = self.lcs_finder.compute_lcs()


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

        map_chars = {
            "A": 0,
            "T": 1,
            "C": 2,
            "G": 3,
            "-": 4
        }  # Mapeia os caracteres de nucleotídeos e o caractere de espaço para valores numéricos (indices).

        # Obtém o comprimento do alinhamento (todas as sequências alinhadas têm o mesmo comprimento).
        alignment_length = len(aligned_seqs[0])

        # Cria a figura do Plotly com um heatmap.
        fig = go.Figure(data=go.Heatmap(
            z=[[map_chars[char] for char in aligned_seq] for aligned_seq in aligned_seqs],  # Converte as sequências alinhadas em valores numéricos.
            x=list(range(alignment_length)),  # Posições no alinhamento (eixo x).
            y=ids,  # IDs das sequências (eixo y).
            text=[list(aligned_seq) for aligned_seq in aligned_seqs],  # Texto a ser exibido em cada célula.
            texttemplate="%{text}",  # Formato para exibir o texto.
            colorscale="Portland",  # Escala de cores.
            showscale=False,  # Oculta a barra de escala de cores.
            xgap=1,  # Espaçamento entre células no eixo x.
            ygap=1,  # Espaçamento entre células no eixo y.
            hovertemplate="ID: %{y}<br>Pos: %{x}<br>Base: %{text}<extra></extra>" # Informação exibida ao passar o mouse.
        ))

        # Configura o layout da figura.
        fig.update_layout(
            title_text="Visualização ilustrando as subsequências conservadas identificadas",
            height=max(400, 200 + len(ids) * 30),
            margin=dict(l=120, r=50, t=100, b=50),
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