from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- New tests targeting the specific bugs we fixed ---

def test_hard_difficulty_harder_than_normal():
    # FIX verified: Hard was 1-50 (easier than Normal 1-100). Now it's 1-150.
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high, "Hard range should be larger (harder) than Normal"

def test_no_string_comparison_trick():
    # FIX verified: The old app.py converted secret to str on even attempts,
    # making "7" > "50" True (lexicographic). check_guess must always use numeric
    # comparison — passing an int secret should never give a wrong result.
    assert check_guess(7, 50) == "Too Low"   # 7 < 50, not "Too High"
    assert check_guess(51, 50) == "Too High"  # 51 > 50

def test_update_score_win_first_attempt():
    # Win on attempt 1 should score 90 (100 - 10*1), not 80 (old off-by-one was 100 - 10*(1+1)).
    score = update_score(0, "Win", 1)
    assert score == 90

def test_update_score_wrong_guess_never_rewards():
    # FIX verified: old code gave +5 for "Too High" on even attempts (rewarding a wrong guess).
    # Now both wrong outcomes always subtract 5.
    score_high = update_score(50, "Too High", 2)
    score_low = update_score(50, "Too Low", 2)
    assert score_high == 45
    assert score_low == 45

def test_parse_guess_valid():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_guess_empty():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None

def test_parse_guess_non_number():
    ok, val, err = parse_guess("abc")
    assert ok is False
