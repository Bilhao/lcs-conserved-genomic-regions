# LCS Conserved Genomic Regions

A Python-based bioinformatics tool for identifying and analyzing conserved genomic regions using global sequence alignment algorithms. This project dynamic programming to find optimal alignments between DNA sequences and identify conserved regions.

## Features

- **Global Sequence Alignment**: Uses dynamic programming for optimal global alignment
- **Multi-sequence Support**: Handles alignment of 2, 3, or N sequences simultaneously
- **Configurable Scoring**: Customizable match scores, mismatch penalties, and gap penalties
- **FASTA File Support**: Load sequences directly from FASTA files
- **Interactive Visualization**: Generate heatmap visualizations of alignments
- **Comprehensive Analysis**: Calculate identity percentages and identify conserved positions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Bilhao/lcs-conserved-genomic-regions.git
cd lcs-conserved-genomic-regions
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the main application for an interactive command-line interface:

```bash
python main.py
```

The interactive interface allows you to:
- Add sequences manually
- Load sequences from FASTA files
- Calculate alignments
- View detailed alignment information
- Generate visualizations

### Programmatic Usage

#### Basic Alignment

```python
from sequence import Sequence
from lcs_finder import LCSFinder

# Create sequences
seq1 = Sequence("seq1", "Human sequence", "ATCGATCGATCG")
seq2 = Sequence("seq2", "Mouse sequence", "ATCGATCGATGG")

# Perform alignment
aligner = LCSFinder(seq1, seq2)
alignment = aligner.compute_lcs()

# Get results
print(f"Alignment score: {alignment.score}")
print(f"Identity: {alignment.identity():.1f}%")
print(f"Aligned sequence 1: {alignment.aligned_seq1}")
print(f"Aligned sequence 2: {alignment.aligned_seq2}")
```

#### Three-Sequence Alignment

```python
from sequence import Sequence
from lcs_finder import LCSFinder

# Create three sequences
seq1 = Sequence("seq1", "Human sequence", "ATCGATCGATCG")
seq2 = Sequence("seq2", "Mouse sequence", "ATCGATCGATGG")
seq3 = Sequence("seq3", "Chimp sequence", "ATCGATCGAACG")

# Perform three-way alignment
aligner = LCSFinder(seq1, seq2, seq3)
alignment = aligner.compute_lcs()

# Get results
print(f"Three-way alignment score: {alignment.score}")
print(f"Identity: {alignment.identity():.1f}%")
```

#### N-Sequence Alignment (4+ sequences)

```python
from sequence import Sequence
from lcs_finder_n_sequences import LCSFinderNSequences

# Create multiple sequences
sequences = [
    Sequence("seq1", "Human sequence", "ATCGATCGATCG"),
    Sequence("seq2", "Mouse sequence", "ATCGATCGATGG"),
    Sequence("seq3", "Chimp sequence", "ATCGATCGAACG"),
    Sequence("seq4", "Rat sequence", "ATCGATCGTTCG"),
    Sequence("seq5", "Dog sequence", "ATCGATCGATAG")
]

# Perform N-way LCS calculation
aligner = LCSFinderNSequences(sequences)
lcs_length = aligner.get_lcs_length()
lcs_sequence = aligner.get_lcs()

print(f"LCS length: {lcs_length}")
print(f"LCS sequence: {lcs_sequence}")
```

**Note**: N-sequence alignment currently supports LCS calculation but not detailed alignment visualization or scoring.

#### Working with FASTA Files

```python
from sequence_database import SequenceDatabase

# Load sequences from FASTA file
db = SequenceDatabase()
db.load_from_fasta("example.fasta")

# Get sequences for alignment
sequences = list(db.database.values())
if len(sequences) >= 2:
    if len(sequences) <= 3:
        aligner = LCSFinder(sequences[0], sequences[1])
        alignment = aligner.compute_lcs()
    else:
        # Use N-sequence LCS for 4+ sequences
        from lcs_finder_n_sequences import LCSFinderNSequences
        aligner = LCSFinderNSequences(sequences)
        lcs_length = aligner.get_lcs_length()
        lcs_sequence = aligner.get_lcs()
```

## Algorithm Details

- **Dynamic Programming**: Uses 2D matrices for pairwise alignment and 3D tensors for three-way alignment
- **Traceback**: Reconstructs optimal alignment by backtracking through the scoring matrix

### Three-Sequence Extension

For three sequences, the algorithm extends to 3D space:
- Uses a 3D tensor instead of a 2D matrix
- Considers all possible alignment combinations
- Maintains optimal substructure property

### N-Sequence LCS Algorithm

For sequences beyond three (N ≥ 4), the implementation uses a specialized LCS algorithm:
- **Dynamic Programming Approach**: Uses multi-dimensional state space
- **Cartesian Product**: Considers all possible index combinations across sequences
- **Optimal Substructure**: Maintains LCS properties across multiple sequences
- **Time Complexity**: O(∏(n_i)) where n_i is the length of sequence i
- **Space Complexity**: O(∏(n_i)) for storing all state combinations

**Current Limitations for N-sequences:**
- LCS calculation and sequence reconstruction available
- Detailed alignment scoring and gap handling not implemented
- Visualization limited to 2-3 sequences
- For research applications requiring detailed alignment of 4+ sequences, consider specialized multiple sequence alignment tools

## File Structure

```
lcs-conserved-genomic-regions/
├── main.py                    # Interactive command-line interface
├── sequence.py                # Sequence class definition
├── lcs_finder.py              # Needleman-Wunsch algorithm implementation
├── lcs_finder_n_sequences.py  # N-sequence LCS implementation
├── sequence_alignment.py      # Alignment result class
├── sequence_database.py       # Sequence database management
├── visualize.py               # Visualization tools
├── example.fasta              # Example FASTA file
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Example Output

```
=== Two-Sequence Alignment ===
Sequence 1: ATCGATCGATCG
Sequence 2: ATCGATCGATGG

> Sequência 1: A T C G A T C G A T C G
> Sequência 2: A T C G A T C G A T G G

> Comprimento do alinhamento = 12
> Posições idênticas nas sequências (✓): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 → total = 11
> Identity = (11 ÷ 12) × 100 ≈ 91.67%
```

## Visualization

The tool includes interactive visualization capabilities using Plotly:

- **Heatmap Display**: Visual representation of sequence alignments
- **Position Highlighting**: Clearly shows conserved and variable positions
- **Interactive Features**: Zoom, pan, and hover for detailed information

## Performance Considerations

- **Time Complexity**: 
  - O(n×m) for two sequences
  - O(n×m×k) for three sequences  
  - O(∏(n_i)) for N sequences where n_i is length of sequence i
- **Space Complexity**: 
  - O(n×m) for two sequences
  - O(n×m×k) for three sequences
  - O(∏(n_i)) for N sequences
- **Recommended Limits**: 
  - Works efficiently with 2-3 sequences up to ~1000 nucleotides
  - For N sequences (4+), practical limit depends on sequence lengths due to exponential space complexity

## Testing

Run the test suite:

```bash
# Basic functionality tests
python test_needleman_wunsch.py

# Integration tests
python test_integration.py
```

## License

This project is open source and available under the MIT License.

## Authors

- **Bilhao**
- **Costinha05**
- **BalaFred7**
- **simeaoversos**
