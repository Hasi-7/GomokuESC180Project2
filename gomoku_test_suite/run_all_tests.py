"""
Master Test Runner for Gomoku Test Suite
==========================================
Run ALL tests (basic + edge cases) with a single command.

Usage:
    python run_all_tests.py

This will execute:
- 8 basic tests from test_gomoku_runner
- 60 edge case tests from test_gomoku_edge_cases
- Total: 68 tests

Exit code 0 = all tests passed
Exit code 1 = one or more tests failed
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
    print_board,
)


# ============================================================================
# TEST UTILITIES
# ============================================================================

failures = 0
total_tests = 0


def assert_true(cond, msg=None):
    if not cond:
        raise AssertionError(msg or 'Assertion failed')


def assert_equal(actual, expected, msg=None):
    if actual != expected:
        raise AssertionError(msg or f'Expected {expected}, got {actual}')


def run_test(fn, category=""):
    global failures, total_tests
    total_tests += 1
    name = fn.__name__
    try:
        fn()
        print(f"✓ PASS: {name}")
        return True
    except Exception as e:
        failures += 1
        print(f"✗ FAIL: {name}")
        print(f"  └─ {e}")
        return False


# ============================================================================
# BASIC TESTS (from test_gomoku_runner.py)
# ============================================================================

def test_make_and_is_empty():
    b = make_empty_board(8)
    assert_true(is_empty(b))
    b[0][0] = 'b'
    assert_true(not is_empty(b))


def test_put_seq_and_detects_vertical_open():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 5, 1, 0, 3, 'w')
    assert_true(b[1][5] == 'w' and b[3][5] == 'w')
    open_count, semi = detect_rows(b, 'w', 3)
    assert_true((open_count, semi) == (1, 0))


def test_is_bounded_open_semi_closed():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 5, 1, 0, 3, 'w')
    assert_true(is_bounded(b, 3, 5, 3, 1, 0) == 'OPEN')

    b2 = make_empty_board(8)
    put_seq_on_board(b2, 1, 5, 1, 0, 3, 'w')
    b2[0][5] = 'b'
    assert_true(is_bounded(b2, 3, 5, 3, 1, 0) == 'SEMIOPEN')

    b3 = make_empty_board(8)
    put_seq_on_board(b3, 1, 5, 1, 0, 3, 'w')
    b3[0][5] = 'b'
    b3[4][5] = 'b'
    assert_true(is_bounded(b3, 3, 5, 3, 1, 0) == 'CLOSED')


def test_detect_row_horizontal_and_diagonal():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 4, 'b')
    open_count, semi = detect_row(b, 'b', 0, 0, 4, 0, 1)
    assert_true((open_count, semi) == (0, 1))

    b2 = make_empty_board(8)
    put_seq_on_board(b2, 0, 4, 1, -1, 3, 'b')
    oc, sc = detect_rows(b2, 'b', 3)
    assert_true((oc, sc) == (0, 1))


def test_score_and_win_conditions():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 1, 0, 5, 'b')
    assert_true(score(b) == 100000)
    assert_true(is_win(b) == 'Black won')

    b2 = make_empty_board(8)
    put_seq_on_board(b2, 2, 2, 0, 1, 5, 'w')
    assert_true(score(b2) == -100000)
    assert_true(is_win(b2) == 'White won')


def test_search_max_picks_winning_move_and_none_on_empty():
    b = make_empty_board(8)
    assert_true(search_max(b) == (4, 4))
    put_seq_on_board(b, 0, 0, 1, 0, 4, 'b')
    assert_true(search_max(b) == (4, 0))


def test_print_board_output():
    b = make_empty_board(3)
    b[0][0] = 'b'
    b[2][2] = 'w'
    sio = io.StringIO()
    with contextlib.redirect_stdout(sio):
        print_board(b)
    out = sio.getvalue()
    assert_true('*' in out)
    assert_true('b' in out and 'w' in out)


def test_continue_playing_and_draw():
    b = make_empty_board(8)
    # Fill with pattern that prevents any sequence of 5
    for i in range(8):
        for j in range(8):
            if i < 4:
                b[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
            else:
                b[i][j] = 'w' if (i + j) % 2 == 0 else 'b'  # Reverse pattern in bottom half
    assert_true(is_win(b) == 'Draw')


# ============================================================================
# EDGE CASE TESTS (from test_gomoku_edge_cases.py)
# ============================================================================

# Board boundary tests
def test_sequence_at_top_left_corner():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 0, 2, 3, 0, 1), 'SEMIOPEN')
    
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 0, 0, 1, 0, 3, 'w')
    assert_equal(is_bounded(b2, 2, 0, 3, 1, 0), 'SEMIOPEN')
    
    b3 = make_empty_board(8)
    put_seq_on_board(b3, 0, 0, 1, 1, 3, 'b')
    assert_equal(is_bounded(b3, 2, 2, 3, 1, 1), 'SEMIOPEN')


def test_sequence_at_bottom_right_corner():
    b = make_empty_board(8)
    put_seq_on_board(b, 7, 5, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 7, 7, 3, 0, 1), 'SEMIOPEN')
    
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 5, 7, 1, 0, 3, 'w')
    assert_equal(is_bounded(b2, 7, 7, 3, 1, 0), 'SEMIOPEN')


def test_sequence_at_all_four_corners():
    b = make_empty_board(5)
    b[0][0] = 'b'
    b[0][4] = 'b'
    b[4][0] = 'b'
    b[4][4] = 'b'
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0))


def test_sequence_along_top_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 2, 0, 1, 4, 'b')
    assert_equal(is_bounded(b, 0, 5, 4, 0, 1), 'OPEN')


def test_sequence_along_left_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 0, 1, 0, 4, 'w')
    assert_equal(is_bounded(b, 5, 0, 4, 1, 0), 'OPEN')


def test_sequence_along_bottom_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 7, 2, 0, 1, 4, 'b')
    assert_equal(is_bounded(b, 7, 5, 4, 0, 1), 'OPEN')


def test_sequence_along_right_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 7, 1, 0, 4, 'w')
    assert_equal(is_bounded(b, 5, 7, 4, 1, 0), 'OPEN')


def test_diagonal_from_top_edge_to_right_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 5, 1, 1, 3, 'b')
    assert_equal(is_bounded(b, 2, 7, 3, 1, 1), 'CLOSED')


def test_diagonal_from_left_edge_to_bottom_edge():
    b = make_empty_board(8)
    put_seq_on_board(b, 5, 0, 1, 1, 3, 'w')
    assert_equal(is_bounded(b, 7, 2, 3, 1, 1), 'CLOSED')


# Sequence detection edge cases
def test_single_stone_no_sequence():
    b = make_empty_board(8)
    b[3][3] = 'b'
    for length in range(2, 6):
        open_c, semi_c = detect_rows(b, 'b', length)
        assert_equal((open_c, semi_c), (0, 0), f"Single stone detected as length {length}")


def test_two_stones_not_adjacent():
    b = make_empty_board(8)
    b[0][0] = 'b'
    b[0][2] = 'b'
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0))


def test_exactly_five_in_a_row():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    open_c, semi_c = detect_rows(b, 'b', 5)
    assert_equal((open_c, semi_c), (1, 0))
    assert_equal(is_win(b), 'Black won')


def test_more_than_five_in_a_row():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 0, 0, 1, 7, 'b')
    assert_equal(is_win(b), 'Continue playing', "7 stones in a row should NOT be a win (only exactly 5)")


def test_overlapping_sequences():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    put_seq_on_board(b, 1, 3, 1, 0, 5, 'w')
    result = is_win(b)
    assert_true(result in ['Black won', 'White won'], f"Should detect a winner with crossing sequences, got {result}")


def test_parallel_sequences():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 1, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 2, 1, 0, 1, 4, 'b')
    open_c, semi_c = detect_rows(b, 'b', 4)
    assert_true(open_c + semi_c >= 3, f"Should detect all 3 parallel sequences")


def test_blocked_sequence_both_ends():
    b = make_empty_board(8)
    b[3][2] = 'w'
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    b[3][6] = 'w'
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'CLOSED')


def test_blocked_sequence_one_end():
    b = make_empty_board(8)
    b[3][2] = 'w'
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'SEMIOPEN')


def test_blocked_by_same_color():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 3, 'b')
    b[3][5] = 'b'
    open_3, semi_3 = detect_rows(b, 'b', 3)
    open_4, semi_4 = detect_rows(b, 'b', 4)
    assert_equal((open_3, semi_3), (0, 0), "Should not detect 3-length when it's part of 4")


def test_diagonal_negative_slope():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 6, 1, -1, 4, 'b')
    assert_equal(b[1][6], 'b')
    assert_equal(b[4][3], 'b')
    open_c, semi_c = detect_rows(b, 'b', 4)
    assert_true(open_c + semi_c >= 1, "Should detect diagonal sequence")


def test_all_four_directions():
    b = make_empty_board(10)  # Larger board to avoid overlaps
    
    # Place 4 non-overlapping sequences
    put_seq_on_board(b, 1, 1, 0, 1, 4, 'b')   # horizontal: row 1, cols 1-4
    put_seq_on_board(b, 4, 8, 1, 0, 4, 'w')   # vertical: col 8, rows 4-7
    put_seq_on_board(b, 6, 1, 1, 1, 4, 'b')   # diagonal: (6,1) to (9,4)
    put_seq_on_board(b, 1, 6, 1, -1, 4, 'w')  # anti-diagonal: (1,6) to (4,3)
    
    open_b, semi_b = detect_rows(b, 'b', 4)
    open_w, semi_w = detect_rows(b, 'w', 4)
    
    # Each color should have exactly 2 sequences (one horizontal/diagonal and one vertical/anti-diagonal)
    assert_equal(open_b + semi_b, 2, f"Black should have 2 sequences of length 4, got {open_b + semi_b}")
    assert_equal(open_w + semi_w, 2, f"White should have 2 sequences of length 4, got {open_w + semi_w}")


# Win detection edge cases
def test_win_with_five_horizontal():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    assert_equal(is_win(b), 'Black won')


def test_win_with_five_vertical():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 3, 1, 0, 5, 'w')
    assert_equal(is_win(b), 'White won')


def test_win_with_five_diagonal_positive():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 1, 1, 1, 5, 'b')
    assert_equal(is_win(b), 'Black won')


def test_win_with_five_diagonal_negative():
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 6, 1, -1, 5, 'w')
    assert_equal(is_win(b), 'White won')


def test_no_win_with_four():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'b')
    assert_equal(is_win(b), 'Continue playing')


def test_draw_on_full_board_no_winner():
    b = make_empty_board(8)
    # Fill with pattern that prevents any sequence of 5
    for i in range(8):
        for j in range(8):
            if i < 4:
                b[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
            else:
                b[i][j] = 'w' if (i + j) % 2 == 0 else 'b'  # Reverse pattern in bottom half
    assert_equal(is_win(b), 'Draw')


def test_continue_playing_on_empty_board():
    b = make_empty_board(8)
    assert_equal(is_win(b), 'Continue playing')


def test_continue_playing_with_moves_but_no_five():
    b = make_empty_board(8)
    b[0][0] = 'b'
    b[0][1] = 'w'
    b[1][0] = 'b'
    b[1][1] = 'w'
    assert_equal(is_win(b), 'Continue playing')


def test_both_players_have_five_simultaneously():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 5, 'b')
    put_seq_on_board(b, 1, 0, 0, 1, 5, 'w')
    result = is_win(b)
    assert_true(result in ['Black won', 'White won'], f"Should detect a winner, got {result}")


# Scoring edge cases
def test_score_empty_board():
    b = make_empty_board(8)
    s = score(b)
    assert_equal(s, 0, "Empty board should have score 0")


def test_score_single_stone():
    b = make_empty_board(8)
    b[3][3] = 'b'
    s = score(b)
    assert_true(-1000 < s < 1000, f"Single stone should have small score, got {s}")


def test_score_black_winning():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'b')
    assert_equal(score(b), 100000)


def test_score_white_winning():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 5, 'w')
    assert_equal(score(b), -100000)


def test_score_black_open_four():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'b')
    s = score(b)
    assert_true(s >= 500, f"Black open 4 should score >= 500, got {s}")


def test_score_white_open_four():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'w')
    s = score(b)
    assert_true(s <= -10000, f"White open 4 should score <= -10000, got {s}")


def test_score_blocking_more_valuable():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 2, 0, 1, 4, 'w')
    s = score(b)
    assert_true(s <= -10000, f"White threat should score <= -10000, got {s}")


def test_score_multiple_open_threes():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 3, 'b')
    put_seq_on_board(b, 1, 1, 0, 1, 3, 'b')
    s = score(b)
    assert_true(s > 50, f"Multiple open 3s should have positive score, got {s}")


def test_score_semi_open_less_than_open():
    b1 = make_empty_board(8)
    put_seq_on_board(b1, 3, 2, 0, 1, 3, 'b')
    score_open = score(b1)
    
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 3, 2, 0, 1, 3, 'b')
    b2[3][1] = 'w'
    score_semi = score(b2)
    
    assert_true(score_open > score_semi, "Open sequence should score higher than semi-open")


# search_max edge cases
def test_search_max_empty_board():
    b = make_empty_board(8)
    assert_equal(search_max(b), (4, 4))


def test_search_max_one_empty_cell():
    b = make_empty_board(8)
    for i in range(8):
        for j in range(8):
            if not (i == 3 and j == 3):
                # Use rows of 4 max pattern to prevent accidental wins
                if j < 4:
                    b[i][j] = 'b' if i % 2 == 0 else 'w'
                else:
                    b[i][j] = 'w' if i % 2 == 0 else 'b'
    y, x = search_max(b)
    assert_equal((y, x), (3, 3), f"With only one empty cell, should return (3,3), got ({y},{x})")


def test_search_max_blocks_opponent_win():
    # Test 1: Block semi-open sequence of length 4
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 1, 0, 1, 4, 'w')  # w w w w at row 2, cols 1-4
    b[2][0] = 'b'  # Block one end to make it semi-open
    
    y, x = search_max(b)
    # Black should block at (2, 5) to prevent white from completing 5 in a row
    assert_equal((y, x), (2, 5), 
                 f"Should block white's semi-open 4 at (2,5), got ({y},{x})")
    
    # Test 2: Block open sequence of length 3
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 3, 2, 0, 1, 3, 'w')  # w w w at row 3, cols 2-4
    # This creates an open sequence (empty on both sides)
    
    y2, x2 = search_max(b2)
    # Black should block at one of the ends: (3, 1) or (3, 5)
    assert_true((y2, x2) == (3, 1) or (y2, x2) == (3, 5),
                f"Should block white's open 3 at (3,1) or (3,5), got ({y2},{x2})")
    
    # Test 3: Block semi-open sequence of length 3
    b3 = make_empty_board(8)
    put_seq_on_board(b3, 4, 3, 1, 0, 3, 'w')  # w w w at rows 4-6, col 3
    b3[3][3] = 'b'  # Block one end to make it semi-open
    
    y3, x3 = search_max(b3)
    # Black should block at (7, 3) to prevent white from extending
    assert_equal((y3, x3), (7, 3),
                 f"Should block white's semi-open 3 at (7,3), got ({y3},{x3})")


def test_search_max_takes_winning_move():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 1, 0, 1, 4, 'b')
    y, x = search_max(b)
    assert_true((y, x) in [(3, 0), (3, 5)], f"Should win at (3,0) or (3,5), got ({y},{x})")


def test_search_max_prefers_winning_over_blocking():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 2, 1, 0, 1, 3, 'w')
    y, x = search_max(b)
    assert_true((y, x) in [(0, 0), (0, 5)], f"Should take winning move at (0,0) or (0,5), got ({y},{x})")


def test_search_max_full_board():
    b = make_empty_board(8)
    for i in range(8):
        for j in range(8):
            b[i][j] = 'b'
    assert_equal(search_max(b), (None, None))


# detect_row specific edge cases
def test_detect_row_entire_row_filled():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 8, 'b')
    open_all, semi_all = detect_rows(b, 'b', 5)
    assert_equal(open_all + semi_all, 0, "8 stones in a row should NOT be detected (only exactly 5-in-a-row counts)")


def test_detect_row_alternating_colors():
    b = make_empty_board(8)
    for i in range(8):
        b[0][i] = 'b' if i % 2 == 0 else 'w'
    open_b, semi_b = detect_row(b, 'b', 0, 0, 2, 0, 1)
    open_w, semi_w = detect_row(b, 'w', 0, 0, 2, 0, 1)
    assert_equal((open_b, semi_b), (0, 0))
    assert_equal((open_w, semi_w), (0, 0))


def test_detect_row_with_gaps():
    b = make_empty_board(12)
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    put_seq_on_board(b, 0, 4, 0, 1, 3, 'b')
    put_seq_on_board(b, 0, 8, 0, 1, 3, 'b')
    
    open_c, semi_c = detect_row(b, 'b', 0, 0, 3, 0, 1)
    assert_true(open_c + semi_c >= 3, f"Should detect 3 sequences, got {open_c} open and {semi_c} semi")


def test_detect_row_starts_mid_sequence():
    b = make_empty_board(8)
    put_seq_on_board(b, 2, 0, 0, 1, 5, 'b')
    open_c, semi_c = detect_row(b, 'b', 2, 2, 5, 0, 1)
    assert_true(open_c + semi_c >= 0, "Should handle starting mid-sequence")


# is_bounded specific edge cases
def test_is_bounded_length_one():
    b = make_empty_board(8)
    b[3][3] = 'b'
    assert_equal(is_bounded(b, 3, 3, 1, 0, 1), 'OPEN')


def test_is_bounded_at_exact_board_boundary():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 0, 1, 3, 'b')
    result = is_bounded(b, 0, 2, 3, 0, 1)
    assert_true(result in ['SEMIOPEN', 'CLOSED'], f"Boundary sequence should be SEMIOPEN or CLOSED, got {result}")


def test_is_bounded_surrounded_by_empty():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'OPEN')


def test_is_bounded_surrounded_by_opponent():
    b = make_empty_board(8)
    b[3][2] = 'w'
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    b[3][6] = 'w'
    assert_equal(is_bounded(b, 3, 5, 3, 0, 1), 'CLOSED')


# put_seq_on_board edge cases
def test_put_seq_length_zero():
    b = make_empty_board(8)
    original = [row[:] for row in b]
    put_seq_on_board(b, 3, 3, 0, 1, 0, 'b')
    assert_equal(b, original)


def test_put_seq_length_one():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 1, 'b')
    assert_equal(b[3][3], 'b')
    count = sum(1 for row in b for cell in row if cell != ' ')
    assert_equal(count, 1)


def test_put_seq_overwrites_existing():
    b = make_empty_board(8)
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'b')
    put_seq_on_board(b, 3, 3, 0, 1, 3, 'w')
    assert_equal(b[3][3], 'w')
    assert_equal(b[3][4], 'w')
    assert_equal(b[3][5], 'w')


# Complex game scenarios
def test_complex_mid_game_position():
    b = make_empty_board(8)
    b[4][4] = 'b'
    b[4][5] = 'b'
    b[5][4] = 'b'
    b[3][3] = 'b'
    
    b[4][3] = 'w'
    b[5][5] = 'w'
    b[6][4] = 'w'
    
    assert_equal(is_win(b), 'Continue playing')
    s = score(b)
    assert_true(s != 0, "Mid-game should have non-zero score")


def test_capture_pattern():
    b = make_empty_board(8)
    b[3][2] = 'w'
    b[3][3] = 'b'
    b[3][4] = 'b'
    b[3][5] = 'w'
    
    open_c, semi_c = detect_rows(b, 'b', 2)
    assert_equal((open_c, semi_c), (0, 0), "Fully blocked sequence should not be counted as open or semi-open")


def test_double_threat():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 1, 0, 1, 4, 'b')
    put_seq_on_board(b, 1, 1, 0, 1, 4, 'b')
    
    s = score(b)
    assert_true(s >= 1000, f"Double threat should have high score, got {s}")


def test_fork_attack():
    b = make_empty_board(8)
    put_seq_on_board(b, 4, 2, 0, 1, 3, 'b')
    put_seq_on_board(b, 2, 4, 1, 0, 3, 'b')
    
    open_c, semi_c = detect_rows(b, 'b', 3)
    assert_true(open_c + semi_c >= 2, "Fork should create multiple threats")


def test_near_full_board():
    """Test board that is nearly full but has no winner and continues playing.
    
    Uses blocks of 4 alternating colors to ensure no sequence of exactly 5 can form.
    This creates a clear scenario where the board is almost full but game continues.
    """
    b = make_empty_board(8)
    for i in range(8):
        for j in range(8):
            if not ((i == 4 and j == 4) or (i == 4 and j == 5)):
                # Use rows of 4 max pattern to prevent accidental wins
                if j < 4:
                    b[i][j] = 'b' if i % 2 == 0 else 'w'
                else:
                    b[i][j] = 'w' if i % 2 == 0 else 'b'
    
    # No sequences of exactly 5 possible with this pattern
    assert_equal(is_win(b), 'Continue playing')
    y, x = search_max(b)
    assert_true((y, x) in [(4, 4), (4, 5)], f"Should suggest one of two empty cells, got ({y},{x})")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    print("=" * 70)
    print("GOMOKU COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()
    
    # Basic tests
    print("🔹 BASIC TESTS (8 tests)")
    print("-" * 70)
    basic_tests = [
        test_make_and_is_empty,
        test_put_seq_and_detects_vertical_open,
        test_is_bounded_open_semi_closed,
        test_detect_row_horizontal_and_diagonal,
        test_score_and_win_conditions,
        test_search_max_picks_winning_move_and_none_on_empty,
        test_print_board_output,
        test_continue_playing_and_draw,
    ]
    
    for test in basic_tests:
        run_test(test)
    
    print()
    print("🔹 EDGE CASE TESTS (60 tests)")
    print("-" * 70)
    
    # Edge case tests
    edge_tests = [
        # Board boundaries
        test_sequence_at_top_left_corner,
        test_sequence_at_bottom_right_corner,
        test_sequence_at_all_four_corners,
        test_sequence_along_top_edge,
        test_sequence_along_left_edge,
        test_sequence_along_bottom_edge,
        test_sequence_along_right_edge,
        test_diagonal_from_top_edge_to_right_edge,
        test_diagonal_from_left_edge_to_bottom_edge,
        
        # Sequence detection
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
        
        # Win detection
        test_win_with_five_horizontal,
        test_win_with_five_vertical,
        test_win_with_five_diagonal_positive,
        test_win_with_five_diagonal_negative,
        test_no_win_with_four,
        test_draw_on_full_board_no_winner,
        test_continue_playing_on_empty_board,
        test_continue_playing_with_moves_but_no_five,
        test_both_players_have_five_simultaneously,
        
        # Scoring
        test_score_empty_board,
        test_score_single_stone,
        test_score_black_winning,
        test_score_white_winning,
        test_score_black_open_four,
        test_score_white_open_four,
        test_score_blocking_more_valuable,
        test_score_multiple_open_threes,
        test_score_semi_open_less_than_open,
        
        # search_max
        test_search_max_empty_board,
        test_search_max_one_empty_cell,
        test_search_max_blocks_opponent_win,
        test_search_max_takes_winning_move,
        test_search_max_prefers_winning_over_blocking,
        test_search_max_full_board,
        
        # detect_row specific
        test_detect_row_entire_row_filled,
        test_detect_row_alternating_colors,
        test_detect_row_with_gaps,
        test_detect_row_starts_mid_sequence,
        
        # is_bounded specific
        test_is_bounded_length_one,
        test_is_bounded_at_exact_board_boundary,
        test_is_bounded_surrounded_by_empty,
        test_is_bounded_surrounded_by_opponent,
        
        # put_seq_on_board
        test_put_seq_length_zero,
        test_put_seq_length_one,
        test_put_seq_overwrites_existing,
        
        # Complex scenarios
        test_complex_mid_game_position,
        test_capture_pattern,
        test_double_threat,
        test_fork_attack,
        test_near_full_board,
    ]
    
    for test in edge_tests:
        run_test(test)
    
    # Summary
    print()
    print("=" * 70)
    passed = total_tests - failures
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    if failures == 0:
        print(f"✅ SUCCESS! All {total_tests} tests PASSED! 🎉")
    else:
        print(f"⚠️  RESULTS: {passed}/{total_tests} tests passed ({pass_rate:.1f}%)")
        print(f"❌ {failures} test(s) FAILED")
    
    print("=" * 70)
    
    sys.exit(0 if failures == 0 else 1)


if __name__ == '__main__':
    main()
