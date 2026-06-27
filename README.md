# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose. — A number-guessing game where the player picks a difficulty, gets a range and limited attempts, and uses "Too High / Too Low" hints to find the secret number.
- [x] Detail which bugs you found.
  - Reversed hints: `check_guess` said "Go HIGHER!" when the guess was too high.
  - Hard difficulty (1–50) was easier than Normal (1–100).
  - New Game button never reset `status`, so the game stayed stuck on "lost" or "won".
  - String-conversion hack: on even attempts, `secret` was cast to `str`, breaking numeric comparison (`"7" > "50"` in Python is `True`).
- [x] Explain what fixes you applied.
  - Moved all game logic into `logic_utils.py`; `app.py` now imports from it.
  - Fixed `check_guess` to return only the outcome string and corrected the hint direction.
  - Changed Hard range to `1–150`.
  - Fixed New Game to reset `status`, `history`, `score`, and use the current difficulty range.
  - Removed the string-conversion block entirely.

## 📸 Demo Walkthrough

1. Open the app (`streamlit run app.py`). The sidebar shows "Normal" difficulty selected by default — range 1–100, 8 attempts allowed.
2. Type `40` in the guess field and click **Submit Guess**. The hint reads "📈 Go HIGHER!" — the secret is above 40.
3. Type `70` and submit. The hint reads "📉 Go LOWER!" — the secret is between 40 and 70. Score drops by 5 for each wrong guess.
4. Type `55` → "📉 Go LOWER!" — narrowed to 40–55.
5. Type `48` → "📈 Go HIGHER!" — narrowed to 48–55.
6. Type `52` → "🎉 Correct!" Balloons appear. Final score is shown based on how many attempts it took.
7. Click **New Game**. The game fully resets — attempts, score, history, and status all clear. The sidebar now controls a fresh secret in the correct difficulty range.

## 🧪 Test Results

```
pytest tests/ -v
============================= test session starts =============================
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_hard_difficulty_harder_than_normal PASSED
tests/test_game_logic.py::test_no_string_comparison_trick PASSED
tests/test_game_logic.py::test_update_score_win_first_attempt PASSED
tests/test_game_logic.py::test_update_score_wrong_guess_never_rewards PASSED
tests/test_game_logic.py::test_parse_guess_valid PASSED
tests/test_game_logic.py::test_parse_guess_empty PASSED
tests/test_game_logic.py::test_parse_guess_non_number PASSED
============================== 10 passed in 0.09s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
