# How to Upload to GitHub

Follow these steps to create a GitHub repository and share with your friends:

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Name it something like: `gomoku-test-suite` or `gomoku-tester`
4. Add a description: "Comprehensive test suite for Gomoku (Five in a Row) implementations"
5. Choose **Public** (so friends can access it)
6. **Don't** initialize with README (we already have one)
7. Click **Create repository**

## Step 2: Upload Files

### Option A: Using GitHub Web Interface (Easiest)

1. On your new repository page, click **uploading an existing file**
2. Drag and drop ALL files from the `gomoku-test-suite` folder:
   - `.gitignore`
   - `gomoku.py`
   - `LICENSE`
   - `QUICKSTART.md`
   - `README.md`
   - `test_gomoku.py`
   - `test_gomoku_edge_cases.py`
   - `test_gomoku_runner.py`
3. Write a commit message: "Initial commit - Gomoku test suite"
4. Click **Commit changes**

### Option B: Using Git Command Line

```bash
# Navigate to the gomoku-test-suite folder
cd gomoku-test-suite

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Gomoku test suite"

# Add your GitHub repository as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Share With Friends

Share the repository URL with your friends:
```
https://github.com/YOUR_USERNAME/gomoku-test-suite
```

They can:
- **Download as ZIP**: Click green "Code" button → "Download ZIP"
- **Clone**: `git clone https://github.com/YOUR_USERNAME/gomoku-test-suite.git`

## Step 4: Tell Friends How to Use It

Send them this message:

---

**🎮 Gomoku Test Suite - Find Bugs in Your Code!**

I created a comprehensive test suite for our Gomoku project. It has 76 tests that check for common bugs and edge cases.

**How to use:**
1. Download from: [YOUR_GITHUB_URL]
2. Replace `gomoku.py` with your implementation
3. Run: `python test_gomoku_runner.py`
4. Fix any failing tests
5. Profit! 🎉

Check the README.md for detailed instructions.

---

## Optional: Add a Nice README Badge

Add this to the top of your README.md to show test count:

```markdown
![Tests](https://img.shields.io/badge/tests-76-brightgreen)
![Python](https://img.shields.io/badge/python-3.6+-blue)
```

## Tips for Maintaining the Repo

- Add a **CONTRIBUTORS.md** file to credit anyone who helps improve the tests
- Use **GitHub Issues** to track bugs or feature requests
- Accept **Pull Requests** if friends want to add more tests
- Keep the README updated with any new features

## Privacy Note

Remember:
- The repository is **public** - anyone can see it
- Don't include your actual homework solutions
- The placeholder `gomoku.py` is intentionally empty
- This is a testing tool, not a solution

---

**Have fun sharing your test suite!** 🚀
