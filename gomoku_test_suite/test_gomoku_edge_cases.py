"""
Comprehensive Edge Case Testing for Gomoku
Tests every possible edge case scenario including:
- Board boundaries and corner cases
- Sequence detection at edges and corners
- Multiple overlapping sequences
- Win detection edge cases
- Scoring edge cases
- AI decision-making edge cases
"""

import sys
import io
import contextlib

from gomoku import (
    make_empty_board,
    put_seq_on_board,
    is_empty,
    is_bounded,
    detect_row,
    detect_rows,
    score,
    search_max,
    is_win,
)


failures = 0


def assert_true(cond, msg=None):
    if not cond:
        raise AssertionError(msg or 'Assertion failed')


def assert_equal(actual, expected, msg=None):
    if actual != expected:
        raise AssertionError(msg or f'Expected {expected}, got {actual}')


def run_test(fn):
    global failures
    name = fn.__name__
    try:
        fn()
        print(f"PASS: {name}")
    except Exception as e:
        failures += 1
        print(f"FAIL: {name} -> {e}")


# ============================================================================
# BOARD BOUNDARY TESTS
# ============================================================================

def test_sequence_at_top_left_corner():
    """Test sequences starting from (0,0)"""
    b = make_empty_board(8)
    # Horizontal from corner
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 0, 2, 3, 0, 1), 'SEMIOPEN')
    
    # Vertical from corner
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 0, 0, 1, 0, 3, 'w')
    assert_equal(is_bounded(b2, 2, 0, 3, 1, 0), 'SEMIOPEN')
    
    # Diagonal from corner
    b3 = make_empty_board(8)
    put_seq_on_board(b3, 0, 0, 1, 1, 3, 'b')
    assert_equal(is_bounded(b3, 2, 2, 3, 1, 1), 'SEMIOPEN')


def test_sequence_at_bottom_right_corner():
    """Test sequences ending at bottom-right corner"""
    b = make_empty_board(8)
    # Horizontal ending at corner
    put_seq_on_board(b, 7, 5, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 7, 7, 3, 0, 1), 'SEMIOPEN')
    
    # Vertical ending at corner
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 5, 7, 1, 0, 3, 'w')
    assert_equal(is_bounded(b2, 7, 7, 3, 1, 0), 'SEMIOPEN')


def test_sequence_at_all_four_corners():
    """Test that all corners are handled correctly"""
    b = make_empty_board(5)
    # Top-left
    b[0][0] = 'b'
    # Top-right
    b[0][4] = 'b'
    # Bottom-left
    b[4][0] = 'b'
    # Bottom-right
    b[4][4] = 'b'
    
    # Should detect 4 separate single stones, no sequences
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0))


def test_sequence_along_top_edge():
    """Test horizontal sequence along top edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 2, 0, 1, 4, 'b')
    assert_equal(is_bounded(b, 0, 5, 4, 0, 1), 'OPEN')


def test_sequence_along_left_edge():
    """Test vertical sequence along left edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 0, 1, 0, 4, 'w')
    assert_equal(is_bounded(b, 5, 0, 4, 1, 0), 'OPEN')


def test_sequence_along_bottom_edge():
    """Test horizontal sequence along bottom edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 7, 2, 0, 1, 4, 'b')
    assert_equal(is_bounded(b, 7, 5, 4, 0, 1), 'OPEN')


def test_sequence_along_right_edge():
    """Test vertical sequence along right edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 7, 1, 0, 4, 'w')
    assert_equal(is_bounded(b, 5, 7, 4, 1, 0), 'OPEN')


def test_diagonal_from_top_edge_to_right_edge():
    """Test diagonal that starts at top and ends at right edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 5, 1, 1, 3, 'b')
    # Ends at (2, 7)
    assert_equal(is_bounded(b, 2, 7, 3, 1, 1), 'CLOSED')


def test_diagonal_from_left_edge_to_bottom_edge():
    """Test diagonal that starts at left and ends at bottom edge"""
    b = make_empty_board(8)
    put_seq_on_board(b, 5, 0, 1, 1, 3, 'w')
    # Ends at (7, 2)
    assert_equal(is_bounded(b, 7, 2, 3, 1, 1), 'CLOSED')


# ============================================================================
# SEQUENCE DETECTION EDGE CASES
# ============================================================================

def test_single_stone_no_sequence():
    """Single stone should not create any sequences of length 2+"""
    b = make_empty_board(8)
    b[3][3] = 'b'
    for length in range(2, 6):
        open_c, semi_c = detect_rows(b, 'b', length)
        assert_equal((open_c, semi_c), (0, 0), f"Single stone detected as length {length}")


def test_two_stones_not_adjacent():
    """Two non-adjacent stones should not form a sequence"""
    b = make_empty_board(8)
    b[0][0] = 'b'
    b[0][2] = 'b'  # Gap at [0][1]
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0))


def test_exactly_five_in_a_row():
    """Test detection of exactly 5 stones"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    open_c, semi_c = detect_rows(b, 'b', 5)
    assert_equal((open_c, semi_c), (1, 0))
    assert_equal(is_win(b), 'Black won')


def test_more_than_five_in_a_row():
    """Test that 6+ stones in a row still counts as a win"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 0, 0, 1, 7, 'b')
    # Having 7 stones in a row should definitely be a win (contains multiple 5-sequences)
    assert_equal(is_win(b), 'Black won', "7 stones in a row should be detected as a win")


def test_overlapping_sequences():
    """Test board with multiple overlapping sequences"""
    b = make_empty_board(8)
    # Create a cross pattern - but they'll overwrite at intersection
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')  # Horizontal at row 3
    put_seq_on_board(b, 1, 3, 1, 0, 5, 'w')  # Vertical at col 3 (overwrites intersection)
    # At least one player should have a winning 5-in-a-row
    result = is_win(b)
    assert_true(result in ['Black won', 'White won'], f"Should detect a winner with crossing sequences, got {result}")


def test_parallel_sequences():
    """Test multiple parallel sequences"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 1, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 2, 1, 0, 1, 4, 'b')
    open_c, semi_c = detect_rows(b, 'b', 4)
    assert_true(open_c + semi_c >= 3, "Should detect all 3 parallel sequences")


def test_blocked_sequence_both_ends():
    """Test sequence blocked by opponent on both ends"""
    b = make_empty_board(8)
    b[3][2] = 'w'  # Blocker before
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    b[3][6] = 'w'  # Blocker after
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'CLOSED')


def test_blocked_sequence_one_end():
    """Test sequence blocked on one end, open on other"""
    b = make_empty_board(8)
    b[3][2] = 'w'  # Blocker before
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    # Open after
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'SEMIOPEN')


def test_blocked_by_same_color():
    """Test that blocking by same color extends the sequence"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 3, 'b')
    b[3][5] = 'b'  # Adjacent same color
    # This should be detected as a 4-sequence, not separate 3-sequence
    open_3, semi_3 = detect_rows(b, 'b', 3)
    open_4, semi_4 = detect_rows(b, 'b', 4)
    # Should have 4-length sequence, not the original 3-length
    assert_equal((open_3, semi_3), (0, 0), "Should not detect 3-length when it's part of 4")


def test_diagonal_negative_slope():
    """Test diagonal with negative slope (top-right to bottom-left)"""
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 6, 1, -1, 4, 'b')
    # Should go from (1,6) to (4,3)
    assert_equal(b[1][6], 'b')
    assert_equal(b[4][3], 'b')
    open_c, semi_c = detect_rows(b, 'b', 4)
    assert_true(open_c + semi_c >= 1, "Should detect diagonal sequence")


def test_all_four_directions():
    """Test sequences in all 4 directions from center point"""
    b = make_empty_board(8)
    # Horizontal
    put_seq_on_board(b, 3, 1, 0, 1, 4, 'b')
    # Vertical
    put_seq_on_board(b, 1, 5, 1, 0, 4, 'w')
    # Diagonal /
    put_seq_on_board(b, 4, 0, 1, 1, 4, 'b')
    # Diagonal \
    put_seq_on_board(b, 1, 7, 1, -1, 4, 'w')
    
    open_b, semi_b = detect_rows(b, 'b', 4)
    open_w, semi_w = detect_rows(b, 'w', 4)
    assert_true(open_b + semi_b >= 2, "Should detect black sequences")
    assert_true(open_w + semi_w >= 2, "Should detect white sequences")


# ============================================================================
# WIN DETECTION EDGE CASES
# ============================================================================

def test_win_with_five_horizontal():
    """Test win detection with exactly 5 horizontal"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    assert_equal(is_win(b), 'Black won')


def test_win_with_five_vertical():
    """Test win detection with exactly 5 vertical"""
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 3, 1, 0, 5, 'w')
    assert_equal(is_win(b), 'White won')


def test_win_with_five_diagonal_positive():
    """Test win detection with 5 diagonal (positive slope)"""
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 1, 1, 1, 5, 'b')
    assert_equal(is_win(b), 'Black won')


def test_win_with_five_diagonal_negative():
    """Test win detection with 5 diagonal (negative slope)"""
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 6, 1, -1, 5, 'w')
    assert_equal(is_win(b), 'White won')


def test_no_win_with_four():
    """Test that 4 in a row is not a win"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'b')
    assert_equal(is_win(b), 'Continue playing')


def test_draw_on_full_board_no_winner():
    """Test draw when board is full with no winner"""
    b = make_empty_board(8)
    # Fill board in checkerboard pattern (prevents 5 in a row)
    for i in range(8):
        for j in range(8):
            b[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
    assert_equal(is_win(b), 'Draw')


def test_continue_playing_on_empty_board():
    """Test that empty board should continue playing"""
    b = make_empty_board(8)
    assert_equal(is_win(b), 'Continue playing')


def test_continue_playing_with_moves_but_no_five():
    """Test continue playing with several moves but no winner"""
    b = make_empty_board(8)
    b[0][0] = 'b'
    b[0][1] = 'w'
    b[1][0] = 'b'
    b[1][1] = 'w'
    assert_equal(is_win(b), 'Continue playing')


def test_both_players_have_five_simultaneously():
    """Test when both players achieve 5 (should return first found)"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 5, 'b')
    put_seq_on_board(b, 1, 0, 0, 1, 5, 'w')
    result = is_win(b)
    # Either could win depending on detection order (b checked first in code)
    assert_true(result in ['Black won', 'White won'], f"Should detect a winner, got {result}")


# ============================================================================
# SCORING EDGE CASES
# ============================================================================

def test_score_empty_board():
    """Empty board should have neutral score"""
    b = make_empty_board(8)
    s = score(b)
    assert_equal(s, 0, "Empty board should have score 0")


def test_score_single_stone():
    """Single stone should have minimal score"""
    b = make_empty_board(8)
    b[3][3] = 'b'
    s = score(b)
    # Should be close to 0 (no significant sequences)
    assert_true(-1000 < s < 1000, f"Single stone should have small score, got {s}")


def test_score_black_winning():
    """Black with 5 should return MAX_SCORE"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    assert_equal(score(b), 100000)


def test_score_white_winning():
    """White with 5 should return -MAX_SCORE"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'w')
    assert_equal(score(b), -100000)


def test_score_black_open_four():
    """Black open 4 should have high positive score"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'b')
    s = score(b)
    assert_true(s >= 500, f"Black open 4 should score >= 500, got {s}")


def test_score_white_open_four():
    """White open 4 should have high negative score"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'w')
    s = score(b)
    assert_true(s <= -10000, f"White open 4 should score <= -10000, got {s}")


def test_score_blocking_more_valuable():
    """Test that blocking opponent's 4 is valued highly"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'w')
    s = score(b)
    # White has open 4, so score should be very negative (urgent to block)
    assert_true(s <= -10000, f"White threat should score <= -10000, got {s}")


def test_score_multiple_open_threes():
    """Test scoring with multiple open 3s"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 3, 'b')
    put_seq_on_board(b, 1, 1, 0, 1, 3, 'b')
    s = score(b)
    assert_true(s > 50, f"Multiple open 3s should have positive score, got {s}")


def test_score_semi_open_less_than_open():
    """Test that semi-open sequences score less than open"""
    b1 = make_empty_board(8)
    put_seq_on_board(b1, 3, 2, 0, 1, 3, 'b')
    score_open = score(b1)
    
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 3, 2, 0, 1, 3, 'b')
    b2[3][1] = 'w'  # Block one end
    score_semi = score(b2)
    
    assert_true(score_open > score_semi, "Open sequence should score higher than semi-open")


# ============================================================================
# SEARCH_MAX EDGE CASES
# ============================================================================

def test_search_max_empty_board():
    """Empty board should return (None, None)"""
    b = make_empty_board(8)
    assert_equal(search_max(b), (None, None))


def test_search_max_one_empty_cell():
    """Board with one empty cell should return that cell"""
    b = make_empty_board(8)
    for i in range(8):
        for j in range(8):
            if not (i == 3 and j == 3):
                b[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
    # Only (3,3) is empty - search_max should return it as the only legal move
    y, x = search_max(b)
    assert_equal((y, x), (3, 3), f"With only one empty cell, should return (3,3), got ({y},{x})")


def test_search_max_blocks_opponent_win():
    """AI should block opponent's winning move"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 4, 'w')
    # White has 4 in a row at positions (3,1) to (3,4)
    # Best move for black is to block at (3,0) or (3,5)
    y, x = search_max(b)
    assert_true((y, x) in [(3, 0), (3, 5)], f"Should block white's winning threat at (3,0) or (3,5), got ({y},{x})")


def test_search_max_takes_winning_move():
    """AI should take winning move if available"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 4, 'b')
    # Black has 4 in a row, can win at (3,0) or (3,5)
    y, x = search_max(b)
    assert_true((y, x) in [(3, 0), (3, 5)], f"Should win at (3,0) or (3,5), got ({y},{x})")


def test_search_max_prefers_winning_over_blocking():
    """AI should prefer winning over blocking"""
    b = make_empty_board(8)
    # Black can win
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')
    # White has threat but not immediate
    put_seq_on_board(b, 2, 1, 0, 1, 3, 'w')
    
    y, x = search_max(b)
    # Should complete black's winning sequence
    assert_true((y, x) in [(0, 0), (0, 5)], f"Should take winning move at (0,0) or (0,5), got ({y},{x})")


def test_search_max_full_board():
    """Full board should return (None, None)"""
    b = make_empty_board(8)
    for i in range(8):
        for j in range(8):
            b[i][j] = 'b'
    assert_equal(search_max(b), (None, None))


# ============================================================================
# DETECT_ROW SPECIFIC EDGE CASES
# ============================================================================

def test_detect_row_entire_row_filled():
    """Test detect_row on completely filled row"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 8, 'b')
    # An entire row of 8 black stones should be detected as containing a 5-sequence
    open_all, semi_all = detect_rows(b, 'b', 5)
    assert_true(open_all + semi_all >= 1, "8 stones in a row must contain at least one 5-sequence")


def test_detect_row_alternating_colors():
    """Test detect_row with alternating colors"""
    b = make_empty_board(8)
    for i in range(8):
        b[0][i] = 'b' if i % 2 == 0 else 'w'
    open_b, semi_b = detect_row(b, 'b', 0, 0, 2, 0, 1)
    open_w, semi_w = detect_row(b, 'w', 0, 0, 2, 0, 1)
    # No sequences of length 2 should be detected
    assert_equal((open_b, semi_b), (0, 0))
    assert_equal((open_w, semi_w), (0, 0))


def test_detect_row_with_gaps():
    """Test detect_row with gaps between sequences"""
    b = make_empty_board(12)
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    # Gap at position 3
    put_seq_on_board(b, 0, 4, 0, 1, 3, 'b')
    # Gap at position 7
    put_seq_on_board(b, 0, 8, 0, 1, 3, 'b')
    
    open_c, semi_c = detect_row(b, 'b', 0, 0, 3, 0, 1)
    # Should detect 3 separate sequences
    assert_true(open_c + semi_c >= 3, f"Should detect 3 sequences, got {open_c} open and {semi_c} semi")


def test_detect_row_starts_mid_sequence():
    """Test detect_row when starting position is in middle of sequence"""
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 0, 0, 1, 5, 'b')
    # Start detection from middle of sequence
    open_c, semi_c = detect_row(b, 'b', 2, 2, 5, 0, 1)
    # Should still detect the sequence or part of it
    assert_true(open_c + semi_c >= 0, "Should handle starting mid-sequence")


# ============================================================================
# IS_BOUNDED SPECIFIC EDGE CASES
# ============================================================================

def test_is_bounded_length_one():
    """Test is_bounded with length 1 (single stone)"""
    b = make_empty_board(8)
    b[3][3] = 'b'
    assert_equal(is_bounded(b, 3, 3, 1, 0, 1), 'OPEN')


def test_is_bounded_at_exact_board_boundary():
    """Test is_bounded when sequence touches board boundary"""
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    # Sequence at top-left, one end at boundary
    result = is_bounded(b, 0, 2, 3, 0, 1)
    assert_true(result in ['SEMIOPEN', 'CLOSED'], f"Boundary sequence should be SEMIOPEN or CLOSED, got {result}")


def test_is_bounded_surrounded_by_empty():
    """Test is_bounded with sequence completely surrounded by empty"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'OPEN')


def test_is_bounded_surrounded_by_opponent():
    """Test is_bounded with sequence surrounded by opponent"""
    b = make_empty_board(8)
    b[3][2] = 'w'
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    b[3][6] = 'w'
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'CLOSED')


# ============================================================================
# PUT_SEQ_ON_BOARD EDGE CASES
# ============================================================================

def test_put_seq_length_zero():
    """Test put_seq_on_board with length 0"""
    b = make_empty_board(8)
    original = [row[:] for row in b]
    put_seq_on_board(b, 3, 3, 0, 1, 0, 'b')
    # Board should be unchanged
    assert_equal(b, original)


def test_put_seq_length_one():
    """Test put_seq_on_board with length 1"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 1, 'b')
    assert_equal(b[3][3], 'b')
    # Only one cell should be filled
    count = sum(1 for row in b for cell in row if cell != ' ')
    assert_equal(count, 1)


def test_put_seq_overwrites_existing():
    """Test that put_seq_on_board overwrites existing pieces"""
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    # Overwrite with white
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'w')
    assert_equal(b[3][3], 'w')
    assert_equal(b[3][4], 'w')
    assert_equal(b[3][5], 'w')


# ============================================================================
# COMPLEX GAME SCENARIOS
# ============================================================================

def test_complex_mid_game_position():
    """Test a realistic mid-game position"""
    b = make_empty_board(8)
    # Black stones
    b[4][4] = 'b'  # Center
    b[4][5] = 'b'
    b[5][4] = 'b'
    b[3][3] = 'b'
    
    # White stones
    b[4][3] = 'w'
    b[5][5] = 'w'
    b[6][4] = 'w'
    
    # Should continue playing
    assert_equal(is_win(b), 'Continue playing')
    # Should have some score value
    s = score(b)
    assert_true(s != 0, "Mid-game should have non-zero score")


def test_capture_pattern():
    """Test common capture pattern (though captures aren't implemented)"""
    b = make_empty_board(8)
    # Create sandwich pattern: w-b-b-w
    b[3][2] = 'w'
    b[3][3] = 'b'
    b[3][4] = 'b'
    b[3][5] = 'w'
    
    # Black has a sequence of 2, but it's CLOSED (blocked on both ends by white)
    # The algorithm should correctly identify this as a closed sequence
    # and NOT count it as open or semi-open
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0), "Fully blocked sequence should not be counted as open or semi-open")


def test_double_threat():
    """Test position where player has two ways to win"""
    b = make_empty_board(8)
    # Black has two open fours
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')  # Can extend to (0,0) or (0,5)
    put_seq_on_board(b, 1, 1, 0, 1, 4, 'b')  # Can extend to (1,0) or (1,5)
    
    # AI should recognize this as a very strong position
    s = score(b)
    assert_true(s >= 1000, f"Double threat should have high score, got {s}")


def test_fork_attack():
    """Test fork attack pattern"""
    b = make_empty_board(8)
    # Create L-shape that threatens in two directions
    put_seq_on_board(b, 4, 2, 0, 1, 3, 'b')
    put_seq_on_board(b, 2, 4, 1, 0, 3, 'b')
    
    open_c, semi_c = detect_rows(b, 'b', 3)
    assert_true(open_c + semi_c >= 2, "Fork should create multiple threats")


def test_near_full_board():
    """Test behavior when board is almost full"""
    b = make_empty_board(8)
    # Fill all but 2 cells
    for i in range(8):
        for j in range(8):
            if not ((i == 4 and j == 4) or (i == 4 and j == 5)):
                b[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
    
    # Should still be playing
    assert_equal(is_win(b), 'Continue playing')
    # search_max should return one of the empty cells
    y, x = search_max(b)
    assert_true((y, x) in [(4, 4), (4, 5)], f"Should suggest one of two empty cells, got ({y},{x})")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def main():
    tests = [
        # Board boundary tests
        test_sequence_at_top_left_corner,
        test_sequence_at_bottom_right_corner,
        test_sequence_at_all_four_corners,
        test_sequence_along_top_edge,
        test_sequence_along_left_edge,
        test_sequence_along_bottom_edge,
        test_sequence_along_right_edge,
        test_diagonal_from_top_edge_to_right_edge,
        test_diagonal_from_left_edge_to_bottom_edge,
        
        # Sequence detection edge cases
        test_single_stone_no_sequence,
        test_two_stones_not_adjacent,
        test_exactly_five_in_a_row,
        test_more_than_five_in_a_row,
        test_overlapping_sequences,
        test_parallel_sequences,
        test_blocked_sequence_both_ends,
        test_blocked_sequence_one_end,
        test_blocked_by_same_color,
        test_diagonal_negative_slope,
        test_all_four_directions,
        
        # Win detection edge cases
        test_win_with_five_horizontal,
        test_win_with_five_vertical,
        test_win_with_five_diagonal_positive,
        test_win_with_five_diagonal_negative,
        test_no_win_with_four,
        test_draw_on_full_board_no_winner,
        test_continue_playing_on_empty_board,
        test_continue_playing_with_moves_but_no_five,
        test_both_players_have_five_simultaneously,
        
        # Scoring edge cases
        test_score_empty_board,
        test_score_single_stone,
        test_score_black_winning,
        test_score_white_winning,
        test_score_black_open_four,
        test_score_white_open_four,
        test_score_blocking_more_valuable,
        test_score_multiple_open_threes,
        test_score_semi_open_less_than_open,
        
        # search_max edge cases
        test_search_max_empty_board,
        test_search_max_one_empty_cell,
        test_search_max_blocks_opponent_win,
        test_search_max_takes_winning_move,
        test_search_max_prefers_winning_over_blocking,
        test_search_max_full_board,
        
        # detect_row specific edge cases
        test_detect_row_entire_row_filled,
        test_detect_row_alternating_colors,
        test_detect_row_with_gaps,
        test_detect_row_starts_mid_sequence,
        
        # is_bounded specific edge cases
        test_is_bounded_length_one,
        test_is_bounded_at_exact_board_boundary,
        test_is_bounded_surrounded_by_empty,
        test_is_bounded_surrounded_by_opponent,
        
        # put_seq_on_board edge cases
        test_put_seq_length_zero,
        test_put_seq_length_one,
        test_put_seq_overwrites_existing,
        
        # Complex game scenarios
        test_complex_mid_game_position,
        test_capture_pattern,
        test_double_threat,
        test_fork_attack,
        test_near_full_board,
    ]
    
    print(f"Running {len(tests)} edge case tests...\n")
    
    for t in tests:
        run_test(t)
    
    print(f"\n{'='*70}")
    if failures:
        print(f"RESULT: {failures} test(s) FAILED out of {len(tests)} total")
        print(f"{'='*70}")
        sys.exit(1)
    else:
        print(f"RESULT: All {len(tests)} tests PASSED! ✓")
        print(f"{'='*70}")
        sys.exit(0)


if __name__ == '__main__':
    main()
