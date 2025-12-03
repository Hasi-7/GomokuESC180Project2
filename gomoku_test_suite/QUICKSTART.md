# Quick Start Guide

## Step 1: Get Your Code
Replace the placeholder `gomoku.py` with your own Gomoku implementation.

## Step 2: Run ALL Tests

### ⭐ The Simple Way (Recommended):
```bash
python run_all_tests.py
```

This single command runs all 68 tests - no pytest, no dependencies, no hassle!

### 📝 Alternative Options (Optional):

If you want to use the separate test files:

```bash
python test_gomoku_runner.py          # Basic tests only (8 tests)
python test_gomoku_edge_cases.py      # Edge cases only (60 tests)
pytest -v                             # All tests with pytest (requires installation)
```

> 💡 **Tip:** You can delete `test_gomoku.py`, `test_gomoku_runner.py`, and `test_gomoku_edge_cases.py` if you only want to use `run_all_tests.py`!

## Step 3: Fix Bugs

When tests fail, they'll tell you exactly what's wrong:
```
FAIL: test_more_than_five_in_a_row -> 7 stones in a row should be detected as a win
```

This means your code doesn't detect 7 consecutive stones as a winning condition.

## Step 4: Rerun Tests

After fixing bugs, run the tests again to verify your fixes!

## Common Issues

**"ModuleNotFoundError: No module named 'gomoku'"**
- Make sure `gomoku.py` is in the same folder as the test files

**"ModuleNotFoundError: No module named 'pytest'"**
- Use `python test_gomoku_runner.py` instead, OR
- Install pytest: `pip install pytest`

**All tests fail immediately**
- Check that your gomoku.py has all the required functions
- See README.md for the full list

## Test Breakdown

- **8 basic tests** - Core functionality
- **60 edge case tests** - Corner cases and potential bugs
- **76 total tests** - Comprehensive validation

## Need Help?

Read the full README.md for:
- Detailed test descriptions
- Common bugs and how to fix them
- How to add your own tests
- Understanding test output

---

Good luck! 🎮
