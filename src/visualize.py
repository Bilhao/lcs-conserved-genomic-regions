from .sequence import Sequence
from .sequence_alignment import SequenceAlignment
from .sequence_database import SequenceDatabase
from .lcs_finder import LCSFinder
from .lcs_finder_n_sequences import LCSFinderNSequences
import plotly.graph_objects as go

class Visualize():
    """
    Classe para visualizar o LCS (Longest Common Subsequence) e o alinhamento de sequências de DNA.
    """
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
    
    def _compute_consensus(self, aligned_seqs):
        """
        Calcula a sequência consenso a partir das sequências alinhadas.
        """
        consensus = []
        alignment_length = len(aligned_seqs[0])
        for i in range(alignment_length):
            column = [seq[i] for seq in aligned_seqs]
            base_counts = {}
            for base in column:
                if base not in base_counts:
                    base_counts[base] = 0
                base_counts[base] += 1
            if base_counts:
                consensus_base = sorted(base_counts.items(), key=lambda x: (-x[1], x[0]))[0][0]
            else:
                consensus_base = "-"
            consensus.append(consensus_base)
        return ''.join(consensus)
    
    def visualize_sequences(self):
        """
        Visualiza o LCS e o alinhamento das sequências usando Plotly.
        """
        ids = list(self.sequence_db.database.keys())

        aligned_seqs = [self.alignment.aligned_seq1, self.alignment.aligned_seq2]
        if self.alignment.aligned_seq3:
            aligned_seqs.append(self.alignment.aligned_seq3)

        consensus = self._compute_consensus(aligned_seqs)
        aligned_seqs.append(consensus)
        ids.append("Consenso")

        map_chars = {
            "A": 0,
            "T": 1,
            "C": 2,
            "G": 3,
            "-": 4
        }

        alignment_length = len(aligned_seqs[0])

        fig = go.Figure(data=go.Heatmap(
            z=[[map_chars.get(char, 4) for char in aligned_seq] for aligned_seq in aligned_seqs],
            x=list(range(alignment_length)),
            y=ids,
            text=[list(aligned_seq) for aligned_seq in aligned_seqs],
            texttemplate="%{text}",
            colorscale="Portland",
            showscale=False,
            xgap=1,
            ygap=1,
            hovertemplate="ID: %{y}<br>Pos: %{x}<br>Base: %{text}<extra></extra>"
        ))

        fig.update_layout(
            title_text="Visualização ilustrando as subsequências conservadas identificadas",
            height=max(400, 200 + len(ids) * 30),
            margin=dict(l=120, r=50, t=100, b=50),
        )

        x_tickvals_dna = list(range(alignment_length))
        x_ticktext_dna = [str(i + 1) for i in x_tickvals_dna]

        fig.update_xaxes(
            showticklabels=True,
            tickvals=x_tickvals_dna,
            ticktext=x_ticktext_dna,
            title_text="Posição no Alinhamento",
            rangeslider_visible=True,
            range=[-0.5, alignment_length - 0.5 if alignment_length < 50 else 49.5]
        )

        fig.update_yaxes(
            autorange="reversed",
            title_text="ID da Sequência"
        )
        
        fig.show(renderer="browser")
