"""
Lightweight test runner for environments without pytest.
Run with: python test_gomoku_runner.py
Exits with code 0 on all tests passing, 1 otherwise.
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


failures = 0


def assert_true(cond, msg=None):
    if not cond:
        raise AssertionError(msg or 'Assertion failed')


def run_test(fn):
    global failures
    name = fn.__name__
    try:
        fn()
        print(f"PASS: {name}")
    except Exception as e:
        failures += 1
        print(f"FAIL: {name} -> {e}")


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
    # sequence at left edge has only one open end -> SEMIOPEN
    assert_true((open_count, semi) == (0, 1))

    b2 = make_empty_board(8)
    put_seq_on_board(b2, 0, 4, 1, -1, 3, 'b')
    # diagonal placed at the top border will be semi-open (only one free end)
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
    assert_true(search_max(b) == (None, None))
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
    b = make_empty_board(4)
    b[0][0] = 'b'
    assert_true(is_win(b) == 'Continue playing')

    b2 = make_empty_board(5)
    for i in range(5):
        for j in range(5):
            b2[i][j] = 'b' if (i + j) % 2 == 0 else 'w'
    assert_true(is_win(b2) == 'Draw')


def main():
    tests = [
        test_make_and_is_empty,
        test_put_seq_and_detects_vertical_open,
        test_is_bounded_open_semi_closed,
        test_detect_row_horizontal_and_diagonal,
        test_score_and_win_conditions,
        test_search_max_picks_winning_move_and_none_on_empty,
        test_print_board_output,
        test_continue_playing_and_draw,
    ]

    for t in tests:
        run_test(t)

    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    else:
        print("\nAll tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
