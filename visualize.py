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
        alignment = self.alignment

        # Use as sequências alinhadas
        aligned_seqs = [alignment.aligned_seq1, alignment.aligned_seq2]
        if alignment.aligned_seq3:
            aligned_seqs.append(alignment.aligned_seq3)

        color_map = {
            'A': 'green',
            'T': 'red',
            'G': 'orange',
            'C': 'blue',
            '-': 'lightgrey',
        }

        sorted_unique_nucleotides = sorted(list(color_map.keys()))
        nucleotide_to_int_idx = {nt: i for i, nt in enumerate(sorted_unique_nucleotides)}
        num_unique_nucleotides = len(sorted_unique_nucleotides)

        # Construa o z e o texto para o heatmap a partir das sequências alinhadas
        z_sequences_indexed = []
        text_sequences = []
        for seq_str in aligned_seqs:
            row = [nucleotide_to_int_idx.get(char_nt, nucleotide_to_int_idx.get('-', 0)) for char_nt in seq_str]
            z_sequences_indexed.append(row)
            text_sequences.append(list(seq_str))

        heatmap_colorscale_dna = []
        colors_in_order_dna = [color_map.get(nt, 'lightgrey') for nt in sorted_unique_nucleotides]
        if num_unique_nucleotides > 0:
            for i in range(num_unique_nucleotides):
                heatmap_colorscale_dna.append([i / num_unique_nucleotides, colors_in_order_dna[i]])
                heatmap_colorscale_dna.append([(i + 1) / num_unique_nucleotides, colors_in_order_dna[i]])
        else:
            heatmap_colorscale_dna = [[0, 'lightgrey'], [1, 'lightgrey']]

        fig_dna = make_subplots(
            rows=2, cols=1,
            row_heights=[0.80, 0.20], # Proporção: 80% para alinhamento, 20% para visão geral
            shared_xaxes=True,
            vertical_spacing=0.3,
            subplot_titles=("Alinhamento de Sequências de DNA", "Visão Geral")
        )

        alignment_length = len(aligned_seqs[0])
        positions_for_plot_dna = list(range(alignment_length))

        # Linha 1: Heatmap do Alinhamento de Sequências
        fig_dna.add_trace(go.Heatmap(
            z=z_sequences_indexed, x=positions_for_plot_dna, y=ids,
            text=text_sequences, texttemplate="%{text}",
            colorscale=heatmap_colorscale_dna, showscale=False,
            xgap=1, ygap=1,
            hovertemplate="ID: %{y}<br>Pos: %{x}<br>Base: %{text}<extra></extra>"
        ), row=1, col=1)

        # Linha 2: Gráfico de Visão Geral (pode ser igual ao alinhamento, ou só mostrar as bases)
        fig_dna.add_trace(go.Heatmap(
            z=z_sequences_indexed, x=positions_for_plot_dna, y=ids,
            colorscale=heatmap_colorscale_dna, showscale=False, hoverinfo='none'
        ), row=2, col=1)

        fig_dna.update_layout(
            title_text="<b>Visualização de Alinhamento de Múltiplas Sequências de DNA</b><br><i>Exemplo com sequências alinhadas</i>",
            height=max(400, 100 + len(ids) * 30 + 100),
            plot_bgcolor='white', font=dict(size=10),
            margin=dict(l=120, r=50, t=100, b=50)
        )

        x_tickvals_dna = list(range(alignment_length))
        x_ticktext_dna = [str(i + 1) for i in x_tickvals_dna]

        fig_dna.update_xaxes(
            showgrid=False, zeroline=False,
            showticklabels=True,
            tickvals=x_tickvals_dna, ticktext=x_ticktext_dna,
            row=1, col=1, title_text="Posição no Alinhamento",
            rangeslider=dict(visible=True)  # Adiciona o rangeslider
        )

        fig_dna.update_xaxes(
            showticklabels=False,
            showgrid=False, zeroline=False,
            row=2, col=1
        )

        fig_dna.update_yaxes(
            autorange="reversed",
            row=1, col=1, title_text="ID da Sequência"
        )

        fig_dna.update_yaxes(
            showticklabels=False,
            autorange="reversed",
            row=2, col=1
        )

        fig_dna.update_traces(textfont_size=12, selector=dict(type='heatmap'), row=1, col=1)
        fig_dna.write_image("alignment_visualization.png", format="png", scale=1)
        #fig_dna.show()