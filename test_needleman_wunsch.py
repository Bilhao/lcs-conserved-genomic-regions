#!/usr/bin/env python3
"""
Test file for Needleman-Wunsch algorithm implementation.
"""

from sequence import Sequence
from lcs_finder import LCSFinder
from sequence_alignment import SequenceAlignment


def test_current_lcs_behavior():
    """Test current LCS behavior before modification."""
    print("=== Testing Current LCS Implementation ===")
    
    # Test case 1: Simple sequences
    seq1 = Sequence("seq1", "Test sequence 1", "ATCG")
    seq2 = Sequence("seq2", "Test sequence 2", "AGTC")
    
    lcs_finder = LCSFinder(seq1, seq2)
    alignment = lcs_finder.compute_lcs()
    
    print(f"Sequence 1: {seq1.seq}")
    print(f"Sequence 2: {seq2.seq}")
    print(f"LCS: {lcs_finder.get_lcs()}")
    print(f"LCS Length: {lcs_finder.get_lcs_length()}")
    print(f"Aligned 1: {alignment.aligned_seq1}")
    print(f"Aligned 2: {alignment.aligned_seq2}")
    print(f"Score from alignment: {alignment.score}")
    print("Alignment details:")
    print(alignment)
    print()


def test_needleman_wunsch_simple():
    """Test basic Needleman-Wunsch functionality."""
    print("=== Testing Needleman-Wunsch Implementation ===")
    
    # Test case: identical sequences should have perfect alignment
    seq1 = Sequence("seq1", "Test sequence 1", "ATCG")
    seq2 = Sequence("seq2", "Test sequence 2", "ATCG")
    
    # This will be updated once we implement Needleman-Wunsch
    lcs_finder = LCSFinder(seq1, seq2)
    alignment = lcs_finder.compute_lcs()
    
    print(f"Sequence 1: {seq1.seq}")
    print(f"Sequence 2: {seq2.seq}")
    print(f"Aligned 1: {alignment.aligned_seq1}")
    print(f"Aligned 2: {alignment.aligned_seq2}")
    print(f"Score from alignment: {alignment.score}")
    print("Alignment details:")
    print(alignment)
    print()


def test_different_sequences():
    """Test with very different sequences."""
    print("=== Testing Different Sequences ===")
    
    seq1 = Sequence("seq1", "Test sequence 1", "AAAA")
    seq2 = Sequence("seq2", "Test sequence 2", "TTTT")
    
    lcs_finder = LCSFinder(seq1, seq2)
    alignment = lcs_finder.compute_lcs()
    
    print(f"Sequence 1: {seq1.seq}")
    print(f"Sequence 2: {seq2.seq}")
    print(f"Score: {lcs_finder.get_lcs_length()}")
    print(f"Aligned 1: {alignment.aligned_seq1}")
    print(f"Aligned 2: {alignment.aligned_seq2}")
    print(f"Score from alignment: {alignment.score}")
    print("Alignment details:")
    print(alignment)
    print()


def test_three_sequences():
    """Test with three sequences."""
    print("=== Testing Three Sequences ===")
    
    seq1 = Sequence("seq1", "Test sequence 1", "ATCG")
    seq2 = Sequence("seq2", "Test sequence 2", "ATCG")
    seq3 = Sequence("seq3", "Test sequence 3", "ATGG")
    
    lcs_finder = LCSFinder(seq1, seq2, seq3)
    alignment = lcs_finder.compute_lcs()
    
    print(f"Sequence 1: {seq1.seq}")
    print(f"Sequence 2: {seq2.seq}")
    print(f"Sequence 3: {seq3.seq}")
    print(f"Score: {lcs_finder.get_lcs_length()}")
    print(f"Aligned 1: {alignment.aligned_seq1}")
    print(f"Aligned 2: {alignment.aligned_seq2}")
    print(f"Aligned 3: {alignment.aligned_seq3}")
    print(f"Score from alignment: {alignment.score}")
    print("Alignment details:")
    print(alignment)
    print()


if __name__ == "__main__":
    test_current_lcs_behavior()
    test_needleman_wunsch_simple()
    test_different_sequences()
    test_three_sequences()