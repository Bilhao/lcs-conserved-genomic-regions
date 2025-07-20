#!/usr/bin/env python3
"""
Debug file for Needleman-Wunsch algorithm implementation.
"""

from sequence import Sequence
from lcs_finder import LCSFinder


def debug_count_matches():
    """Debug the count matches function."""
    print("=== Debug Count Matches ===")
    
    seq1 = Sequence("seq1", "Test sequence 1", "ATCG")
    seq2 = Sequence("seq2", "Test sequence 2", "ATCG")
    
    lcs_finder = LCSFinder(seq1, seq2)
    aligned1, aligned2, aligned3 = lcs_finder._needleman_wunsch_traceback(lcs_finder.dp)
    
    print(f"Aligned 1: '{aligned1}'")
    print(f"Aligned 2: '{aligned2}'")
    print(f"Aligned 3: '{aligned3}'")
    
    matches = 0
    for i, (a, b) in enumerate(zip(aligned1, aligned2)):
        print(f"Position {i}: '{a}' vs '{b}' -> match: {a == b and a != '-'}")
        if a == b and a != '-':
            matches += 1
    
    print(f"Total matches: {matches}")
    

if __name__ == "__main__":
    debug_count_matches()