import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# ── Design System ─────────────────────────────────────────────────────────────

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Russo+One&family=Chakra+Petch:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300&display=swap');

:root {
    --bg:       #0F0F23;
    --surface:  #13132E;
    --surface2: #1B1B42;
    --primary:  #7C3AED;
    --prim-lt:  #A78BFA;
    --cta:      #F43F5E;
    --cta-lt:   #FB7185;
    --text:     #E2E8F0;
    --muted:    #64748B;
    --border:   rgba(124,58,237,0.28);
    --success:  #10B981;
    --r:        10px;
    --glow-p:   0 0 18px rgba(124,58,237,0.4), 0 0 36px rgba(124,58,237,0.12);
    --glow-r:   0 0 18px rgba(244,63,94,0.4),  0 0 36px rgba(244,63,94,0.12);
    --glow-g:   0 0 18px rgba(16,185,129,0.4), 0 0 36px rgba(16,185,129,0.12);
}

/* ── Base ──────────────────────────────────────────── */
.stApp {
    background-color: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 90% 55% at 50% 0%,
            rgba(124,58,237,0.18) 0%, transparent 65%) !important;
    color: var(--text) !important;
    font-family: 'Chakra Petch', sans-serif !important;
}

* { font-family: 'Chakra Petch', sans-serif !important; }
h1, h2, h3, h4 { font-family: 'Russo One', sans-serif !important; }

/* ── Hide Streamlit chrome ─────────────────────────── */
#MainMenu              { display: none !important; }
footer                 { display: none !important; }
[data-testid="stHeader"]     { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"]    { display: none !important; }

/* ── Main content ──────────────────────────────────── */
.main .block-container {
    padding-top: 2.2rem !important;
    max-width: 780px !important;
}

/* ── Sidebar ───────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stSidebar"] h2 {
    font-family: 'Russo One', sans-serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: var(--prim-lt) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: var(--r) !important;
}

/* ── Buttons ───────────────────────────────────────── */
.stButton > button {
    font-family: 'Russo One', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: var(--prim-lt) !important;
    border: 1px solid var(--primary) !important;
    border-radius: var(--r) !important;
    padding: 0.55rem 0.9rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s, box-shadow 0.2s, border-color 0.2s,
                color 0.2s, transform 0.15s !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}

.stButton > button:hover {
    background: rgba(124,58,237,0.14) !important;
    box-shadow: var(--glow-p) !important;
    border-color: var(--prim-lt) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* Submit button — CTA/rose accent */
[data-testid="stColumn"]:nth-child(1) .stButton > button {
    color: var(--cta) !important;
    border-color: var(--cta) !important;
}

[data-testid="stColumn"]:nth-child(1) .stButton > button:hover {
    background: rgba(244,63,94,0.14) !important;
    box-shadow: var(--glow-r) !important;
    border-color: var(--cta-lt) !important;
    color: #fff !important;
}

/* Submit — paper-plane icon */
[data-testid="stColumn"]:nth-child(1) .stButton > button::before {
    content: "";
    display: inline-block;
    width: 15px;
    height: 15px;
    flex-shrink: 0;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23F43F5E' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='22' y1='2' x2='11' y2='13'/%3E%3Cpolygon points='22 2 15 22 11 13 2 9 22 2'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
}

[data-testid="stColumn"]:nth-child(1) .stButton > button:hover::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='22' y1='2' x2='11' y2='13'/%3E%3Cpolygon points='22 2 15 22 11 13 2 9 22 2'/%3E%3C/svg%3E");
}

/* New Game — refresh icon */
[data-testid="stColumn"]:nth-child(2) .stButton > button::before {
    content: "";
    display: inline-block;
    width: 15px;
    height: 15px;
    flex-shrink: 0;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23A78BFA' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='23 4 23 10 17 10'/%3E%3Cpath d='M20.49 15a9 9 0 1 1-2.12-9.36L23 10'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
}

[data-testid="stColumn"]:nth-child(2) .stButton > button:hover::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='23 4 23 10 17 10'/%3E%3Cpath d='M20.49 15a9 9 0 1 1-2.12-9.36L23 10'/%3E%3C/svg%3E");
}

/* ── Text Input ────────────────────────────────────── */
.stTextInput > div > div > input,
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stTextInput > div > div > input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important;
    outline: none !important;
}

.stTextInput label,
[data-testid="stTextInput"] label {
    font-size: 0.7rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Selectbox ─────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
}

/* ── Checkbox ──────────────────────────────────────── */
.stCheckbox label span:last-child {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
}

/* ── Expander ──────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] details {
    border: none !important;
    background: transparent !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    padding: 0.7rem 1rem !important;
    cursor: pointer !important;
    list-style: none !important;
}

/* Kill browser default marker and any leaked Streamlit internal label spans */
[data-testid="stExpander"] summary::-webkit-details-marker { display: none !important; }
[data-testid="stExpander"] summary::marker { content: none !important; }
/* Force SVG chevron color inside summary */
[data-testid="stExpander"] summary svg { color: var(--muted) !important; }

/* ── Divider ───────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.6rem 0 !important;
}

/* ── Alert overrides ───────────────────────────────── */
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    font-family: 'Chakra Petch', sans-serif !important;
}

/* ── Markdown text ─────────────────────────────────── */
[data-testid="stMarkdownContainer"] p {
    color: var(--text) !important;
}

/* ── Scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ── Animations ────────────────────────────────────── */
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes glitch {
    0%   { clip-path: inset(0 0 98% 0); transform: translate(-2px, 0); }
    5%   { clip-path: inset(30% 0 50% 0); transform: translate(2px, 0); }
    10%  { clip-path: inset(70% 0 10% 0); transform: translate(-1px, 0); }
    15%  { clip-path: inset(0 0 0 0); transform: translate(0, 0); }
    100% { clip-path: inset(0 0 0 0); transform: translate(0, 0); }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition-duration: 0.01ms !important;
    }
}

/* ── Custom components ─────────────────────────────── */

.game-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding-bottom: 24px;
    margin-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

.game-header-icon {
    flex-shrink: 0;
    color: var(--primary);
    filter: drop-shadow(0 0 12px rgba(124,58,237,0.75));
    position: relative;
}

.game-header-icon::after {
    content: "";
    position: absolute;
    inset: -4px;
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 12px;
    pointer-events: none;
}

.game-title-h1 {
    margin: 0 0 6px 0;
    font-family: 'Russo One', sans-serif !important;
    font-size: 1.85rem !important;
    line-height: 1.1;
    background: linear-gradient(135deg,
        #ffffff 0%,
        var(--prim-lt) 55%,
        var(--cta) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.01em;
}

.game-glitch {
    position: relative;
    display: inline-block;
}

.game-glitch::before {
    content: attr(data-text);
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, var(--cta) 0%, var(--prim-lt) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: glitch 6s 2s infinite;
    opacity: 0.6;
}

.game-subtitle {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0;
}

.section-label {
    font-family: 'Russo One', sans-serif !important;
    font-size: 0.65rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 20px 0 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

.info-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 18px;
    background: rgba(124,58,237,0.07);
    border: 1px solid var(--border);
    border-radius: var(--r);
    margin: 10px 0;
    color: var(--prim-lt);
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}

.info-bar svg { flex-shrink: 0; }

.outcome-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 20px;
    border-radius: var(--r);
    border: 1px solid;
    margin: 10px 0;
    font-family: 'Russo One', sans-serif !important;
    font-size: 1.1rem;
    letter-spacing: 0.06em;
    animation: slideIn 0.25s ease;
}

.outcome-card svg { flex-shrink: 0; }

.outcome-card.win {
    background: rgba(16,185,129,0.09);
    border-color: rgba(16,185,129,0.45);
    color: #34D399;
    box-shadow: var(--glow-g);
}

.outcome-card.higher {
    background: rgba(124,58,237,0.09);
    border-color: rgba(124,58,237,0.4);
    color: var(--prim-lt);
    box-shadow: var(--glow-p);
}

.outcome-card.lower {
    background: rgba(244,63,94,0.09);
    border-color: rgba(244,63,94,0.4);
    color: var(--cta-lt);
    box-shadow: var(--glow-r);
}

.outcome-card.lost {
    background: rgba(239,68,68,0.09);
    border-color: rgba(239,68,68,0.4);
    color: #FCA5A5;
    box-shadow: 0 0 18px rgba(239,68,68,0.28);
}

.outcome-card.warn {
    background: rgba(245,158,11,0.09);
    border-color: rgba(245,158,11,0.4);
    color: #FCD34D;
}

.game-footer {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 6px;
    opacity: 0.55;
}
</style>
"""

# ── SVG Icon Builder ──────────────────────────────────────────────────────────

def _svg(body: str, w: int = 24, h: int = 24, sw: float = 2.5) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
        f'{body}</svg>'
    )

# Crosshair — investigator / header
ICON_CROSSHAIR = _svg(
    '<circle cx="12" cy="12" r="10"/>'
    '<circle cx="12" cy="12" r="4"/>'
    '<line x1="21.17" y1="12" x2="15" y2="12"/>'
    '<line x1="9" y1="12" x2="2.83" y2="12"/>'
    '<line x1="12" y1="2.83" x2="12" y2="9"/>'
    '<line x1="12" y1="15" x2="12" y2="21.17"/>',
    w=44, h=44, sw=1.6,
)

# Target/navigator — Correct
ICON_TARGET = _svg(
    '<circle cx="12" cy="12" r="10"/>'
    '<polyline points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
)

# Arrow up — Go Higher
ICON_ARROW_UP = _svg(
    '<line x1="12" y1="19" x2="12" y2="5"/>'
    '<polyline points="5 12 12 5 19 12"/>',
)

# Arrow down — Go Lower
ICON_ARROW_DOWN = _svg(
    '<line x1="12" y1="5" x2="12" y2="19"/>'
    '<polyline points="19 12 12 19 5 12"/>',
)

# Info circle — range bar
ICON_INFO = _svg(
    '<circle cx="12" cy="12" r="10"/>'
    '<line x1="12" y1="8" x2="12" y2="12"/>'
    '<line x1="12" y1="16" x2="12.01" y2="16"/>',
    sw=2.0,
)

# Warning triangle — parse errors
ICON_WARN = _svg(
    '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
    '<line x1="12" y1="9" x2="12" y2="13"/>'
    '<line x1="12" y1="17" x2="12.01" y2="17"/>',
    sw=2.0,
)

# Skull — game over
ICON_SKULL = _svg(
    '<circle cx="12" cy="11" r="7"/>'
    '<path d="M9 17v1a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-1"/>'
    '<line x1="9.5" y1="11.5" x2="9.51" y2="11.5" stroke-width="3"/>'
    '<line x1="14.5" y1="11.5" x2="14.51" y2="11.5" stroke-width="3"/>',
    sw=2.0,
)

# ── Render Helpers ────────────────────────────────────────────────────────────

def render_outcome(outcome: str) -> None:
    cfg = {
        "Win":      (ICON_TARGET,     "Correct!",  "win"),
        "Too Low":  (ICON_ARROW_UP,   "Go Higher", "higher"),
        "Too High": (ICON_ARROW_DOWN, "Go Lower",  "lower"),
    }
    icon, label, cls = cfg.get(outcome, ("", outcome, ""))
    st.markdown(
        f'<div class="outcome-card {cls}">{icon}<span>{label}</span></div>',
        unsafe_allow_html=True,
    )

def render_info(text: str) -> None:
    st.markdown(
        f'<div class="info-bar">{ICON_INFO}<span>{text}</span></div>',
        unsafe_allow_html=True,
    )

def render_result(kind: str, text: str) -> None:
    if kind == "success":
        icon, cls = ICON_TARGET, "win"
    elif kind == "warn":
        icon, cls = ICON_WARN, "warn"
    else:
        icon, cls = ICON_SKULL, "lost"
    st.markdown(
        f'<div class="outcome-card {cls}">{icon}<span>{text}</span></div>',
        unsafe_allow_html=True,
    )

# ── App Config ────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Glitch Investigator", layout="centered")
st.markdown(_CSS, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="game-header">
    <div class="game-header-icon">{ICON_CROSSHAIR}</div>
    <div>
        <p class="game-title-h1">
            <span class="game-glitch" data-text="Game Glitch Investigator">
                Game Glitch Investigator
            </span>
        </p>
        <p class="game-subtitle">An AI-generated guessing game &mdash; something is off.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ── Session State ─────────────────────────────────────────────────────────────

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

# ── Game UI ───────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">Make a Guess</p>', unsafe_allow_html=True)

render_info(
    f"Guess a number between {low} and {high} &mdash; "
    f"{attempt_limit - st.session_state.attempts} attempt(s) remaining."
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Reset all session state fields including status and history so the game
# actually becomes playable again after a win or loss.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        render_result("success", "You already won. Start a new game to play again.")
    else:
        render_result("error", "Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        render_result("warn", err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: Removed the intentional string-conversion hack that ran on every
        # even attempt, which caused check_guess to do a lexicographic string
        # comparison and produce wrong hints.
        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            render_outcome(outcome)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            render_result(
                "success",
                f"You cracked it! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                render_result(
                    "error",
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}",
                )

st.divider()
st.markdown(
    '<p class="game-footer">Built by an AI that claims this code is production-ready.</p>',
    unsafe_allow_html=True,
)
