def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was returning 1-50 (easier than Normal). Changed to 1-150 so Hard is actually harder.
    if difficulty == "Hard":
        return 1, 150
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: Refactored from app.py. Now returns only the outcome string (not a tuple)
# so it matches the test interface in tests/test_game_logic.py.
# Previous version had the messages backwards: guess > secret said "Go HIGHER!" (wrong).
def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    # FIXME: Logic breaks here — original code swapped "Go HIGHER!" / "Go LOWER!" messages
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Removed the extra +1 offset that made attempt 1 score only 80 instead of 90.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Removed the even-attempt +5 reward for wrong guesses (was rewarding mistakes).
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
