import pytest

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


def test_make_and_is_empty():
    b = make_empty_board(8)
    assert is_empty(b)
    b[0][0] = 'b'
    assert not is_empty(b)


def test_put_seq_and_detects_vertical_open():
    b = make_empty_board(8)
    # vertical sequence at x=5, y=1..3 (length 3), open at both ends
    put_seq_on_board(b, 1, 5, 1, 0, 3, 'w')
    assert b[1][5] == 'w' and b[3][5] == 'w'
    open_count, semi = detect_rows(b, 'w', 3)
    assert (open_count, semi) == (1, 0)


def test_is_bounded_open_semi_closed():
    # OPEN
    b = make_empty_board(8)
    put_seq_on_board(b, 1, 5, 1, 0, 3, 'w')
    assert is_bounded(b, 3, 5, 3, 1, 0) == 'OPEN'

    # SEMIOPEN - block before
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 1, 5, 1, 0, 3, 'w')
    b2[0][5] = 'b'
    assert is_bounded(b2, 3, 5, 3, 1, 0) == 'SEMIOPEN'

    # CLOSED - block both ends
    b3 = make_empty_board(8)
    put_seq_on_board(b3, 1, 5, 1, 0, 3, 'w')
    b3[0][5] = 'b'
    b3[4][5] = 'b'
    assert is_bounded(b3, 3, 5, 3, 1, 0) == 'CLOSED'


def test_detect_row_horizontal_and_diagonal():
    b = make_empty_board(8)
    # horizontal 4 at top-left
    put_seq_on_board(b, 0, 0, 0, 1, 4, 'b')
    open_count, semi = detect_row(b, 'b', 0, 0, 4, 0, 1)
    # sequence at left edge has only one open end -> SEMIOPEN
    assert (open_count, semi) == (0, 1)

    # diagonal top-right to bottom-left
    b2 = make_empty_board(8)
    put_seq_on_board(b2, 0, 4, 1, -1, 3, 'b')
    # diagonal placed at the top border will be semi-open (only one free end)
    oc, sc = detect_rows(b2, 'b', 3)
    assert (oc, sc) == (0, 1)


def test_score_and_win_conditions():
    b = make_empty_board(8)
    put_seq_on_board(b, 0, 0, 1, 0, 5, 'b')
    assert score(b) == 100000
    assert is_win(b) == 'Black won'

    b2 = make_empty_board(8)
    put_seq_on_board(b2, 2, 2, 0, 1, 5, 'w')
    assert score(b2) == -100000
    assert is_win(b2) == 'White won'


def test_search_max_picks_winning_move_and_none_on_empty():
    b = make_empty_board(8)
    # empty board -> no decisive best move (function returns (None, None))
    assert search_max(b) == (None, None)

    # setup winning move for black: 4 in a column, empty at y=4
    put_seq_on_board(b, 0, 0, 1, 0, 4, 'b')
    # available winning pos at (4,0)
    assert search_max(b) == (4, 0)


def test_print_board_output(capsys):
    b = make_empty_board(3)
    b[0][0] = 'b'
    b[2][2] = 'w'
    print_board(b)
    captured = capsys.readouterr()
    assert '*' in captured.out
    assert 'b' in captured.out and 'w' in captured.out


def test_continue_playing_and_draw():
    # Continue playing: at least one empty cell
    b = make_empty_board(4)
    b[0][0] = 'b'
    assert is_win(b) == 'Continue playing'

    # Draw: fill board with no five-in-row (small board fully filled)
    b2 = make_empty_board(5)
    for i in range(5):
        for j in range(5):
            b2[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
    assert is_win(b2) == 'Draw'
