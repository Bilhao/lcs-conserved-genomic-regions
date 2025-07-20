#!/usr/bin/env python3
"""
Quick integration test for the main application.
"""

from sequence import Sequence
from sequence_database import SequenceDatabase
from lcs_finder import LCSFinder


def test_main_integration():
    """Test integration with main application components."""
    print("=== Testing Main Application Integration ===")
    
    # Create a sequence database
    db = SequenceDatabase()
    
    # Add some test sequences
    seq1 = Sequence("SEQ1", "Human sequence", "ATCGATCGATCG")
    seq2 = Sequence("SEQ2", "Mouse sequence", "ATCGATCGATGG")
    seq3 = Sequence("SEQ3", "Chimp sequence", "ATCGATCGAACG")
    
    db.add_sequence(seq1)
    db.add_sequence(seq2)
    db.add_sequence(seq3)
    
    print(f"Added {len(db.database)} sequences to database")
    
    # Test 2-sequence alignment
    lcs_finder_2 = LCSFinder(seq1, seq2)
    alignment_2 = lcs_finder_2.compute_lcs()
    print(f"\n2-sequence alignment score: {alignment_2.score}")
    print(f"2-sequence identity: {alignment_2.identity():.1f}%")
    
    # Test 3-sequence alignment
    lcs_finder_3 = LCSFinder(seq1, seq2, seq3)
    alignment_3 = lcs_finder_3.compute_lcs()
    print(f"3-sequence alignment score: {alignment_3.score}")
    print(f"3-sequence identity: {alignment_3.identity():.1f}%")
    
    print("\nIntegration test successful!")


if __name__ == "__main__":
    test_main_integration()