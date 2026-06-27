# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  - It looked okay

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  
  - The higher/lower hints are broken. It doesn't make sense that I need to "go higher" when I type in 50 if the max IS 50.
  - The "hard" difficulty shows the numbers 1-50, whilst the "normal" difficulty shows the numbers 1-100, which makes no sense. It should be a higher interval of numbers like 1-150.
  - Extra bug: Once I click "New Game" after losing, I can't restart the game. It only restarts the game and scores when I refresh the page.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret is 50 | "Too High — Go LOWER!" hint | "Go HIGHER!" shown (backwards) | none |
| Select "Hard" difficulty | Range 1–150 (harder than Normal 1–100) | Range 1–50 shown (easier than Normal!) | none |
| Click "New Game" after losing | Game resets and lets me play again | "Game over. Start a new game." shown immediately — game never resets | none |
| Guess 7 on even-numbered attempt, secret is 50 | "Too Low" (7 < 50) | "Too High" shown due to string comparison: "7" > "50" is True in Python | none |




---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Claude suggested moving all four functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py` and importing them in `app.py`. This was correct — it separated UI from logic cleanly, and running `pytest` afterwards showed 10/10 tests passing, including the 3 original starter tests.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - Claude initially described the string-conversion bug as a "state bug where the secret resets." That framing was misleading — the secret never actually changed, it was temporarily cast to a string (`secret = str(st.session_state.secret)`) inside the submit handler on even attempts. I verified this by adding `st.write("secret type:", type(secret))` in the debug panel and confirming it alternated between `int` and `str` each click.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I used two checks: `pytest` to confirm the logic was mathematically correct, then ran `streamlit run app.py` to confirm the live game behaved as expected (hints matched, New Game worked, Hard showed a larger range).
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - `test_no_string_comparison_trick` specifically checks that `check_guess(7, 50)` returns `"Too Low"`, not `"Too High"`. Before the fix, this would have failed because the old app code passed `"50"` (a string) to `check_guess` on even attempts, making Python do `"7" > "50"` → `True` (lexicographic order), returning the wrong outcome.
- Did AI help you design or understand any tests? How?
  - Yes — Claude explained that the string-comparison bug needed a test that specifically used a digit like `7` against a two-digit number like `50`, because that's the case where lexicographic order diverges from numeric order. That insight shaped the exact values used in `test_no_string_comparison_trick`.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? This could be a testing habit, a prompting strategy, or a way you used Git.
  - 
- What is one thing you would do differently next time you work with AI on a coding task?
  - 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - 

prompt or something: 
please work inside the project we're working on "C:\JUAN\Dev\CodePath\AI101\Unit 1\ai110-module1show-gameglitchinvestigator-starter>"

Let's work on the bugs that I typed out in "reflection.md" when trying out the game. let's work on those, before implementing anything else. Before fixing code, explain to me why it's broken and how you would fix it, then go on from there. 