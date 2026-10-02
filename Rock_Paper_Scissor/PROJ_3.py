import streamlit as st
import random
import streamlit.components.v1 as components

# ==============================================================================
# 🎮 ROCK PAPER SCISSORS - CHAMPIONSHIP ARENA (ULTRA-POLISHED EDITION)
# Designed with 10+ Years Senior UI/UX Experience:
# - Dynamic Atmosphere Theming (5 Curated Ambient Themes: Cosmic, Synthwave, Abyss, Aurora, Dragon)
# - Grand Championship Winning Celebration (Canvas Confetti Starbursts, Web Audio Fanfare, Golden Podium)
# - Head-to-Head Visual Scoreboard with Live Real-Time Progress Gauges
# - Dynamic Duel Arena with Clash Feedback & Contextual Battle Commentary
# - Tactical Analytics Hub (Win Rate, Peak Streak, Stalemates, Round History Feed)
# - Tactile Weapon Action Deck with Micro-Interactions
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Rock Paper Scissors • Arena",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Cross-version rerun compatibility helper
def trigger_rerun():
    """Trigger UI update compatible across all Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# ------------------------------------------------------------------------------
# 2. ATMOSPHERIC THEMES SYSTEM
# ------------------------------------------------------------------------------
THEMES = {
    "🌌 Cyber Cosmic": {
        "name": "Cyber Cosmic",
        "bg": "radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.22) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(168, 85, 247, 0.22) 0%, transparent 50%), radial-gradient(circle at 50% 50%, #0d1322 0%, #060911 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(6, 9, 17, 0.98) 100%)",
        "card_bg": "linear-gradient(145deg, rgba(30, 41, 59, 0.72), rgba(15, 23, 42, 0.88))",
        "primary": "#818cf8",
        "accent": "#c084fc",
        "glow": "rgba(168, 85, 247, 0.35)",
        "border": "rgba(168, 85, 247, 0.25)",
        "badge_bg": "linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.3))",
        "badge_color": "#d8b4fe"
    },
    "⚡ Synthwave Sunset": {
        "name": "Synthwave Sunset",
        "bg": "radial-gradient(ellipse at 25% 15%, rgba(244, 63, 94, 0.25) 0%, transparent 50%), radial-gradient(ellipse at 75% 85%, rgba(6, 182, 212, 0.22) 0%, transparent 50%), radial-gradient(circle at 50% 50%, #160a22 0%, #08030e 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(26, 10, 36, 0.96) 0%, rgba(8, 3, 14, 0.98) 100%)",
        "card_bg": "linear-gradient(145deg, rgba(45, 18, 62, 0.68), rgba(16, 6, 25, 0.88))",
        "primary": "#f43f5e",
        "accent": "#06b6d4",
        "glow": "rgba(244, 63, 94, 0.4)",
        "border": "rgba(244, 63, 94, 0.3)",
        "badge_bg": "linear-gradient(135deg, rgba(244, 63, 94, 0.25), rgba(217, 70, 239, 0.3))",
        "badge_color": "#f472b6"
    },
    "🌊 Oceanic Abyss": {
        "name": "Oceanic Abyss",
        "bg": "radial-gradient(ellipse at 25% 25%, rgba(14, 165, 233, 0.24) 0%, transparent 50%), radial-gradient(ellipse at 75% 75%, rgba(20, 184, 166, 0.22) 0%, transparent 50%), radial-gradient(circle at 50% 50%, #05192d 0%, #020b14 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(5, 28, 48, 0.96) 0%, rgba(2, 11, 20, 0.98) 100%)",
        "card_bg": "linear-gradient(145deg, rgba(8, 47, 73, 0.65), rgba(3, 20, 36, 0.88))",
        "primary": "#38bdf8",
        "accent": "#2dd4bf",
        "glow": "rgba(56, 189, 248, 0.35)",
        "border": "rgba(56, 189, 248, 0.25)",
        "badge_bg": "linear-gradient(135deg, rgba(14, 165, 233, 0.25), rgba(20, 184, 166, 0.3))",
        "badge_color": "#7dd3fc"
    },
    "🌲 Aurora Emerald": {
        "name": "Aurora Emerald",
        "bg": "radial-gradient(ellipse at 50% 15%, rgba(16, 185, 129, 0.25) 0%, transparent 55%), radial-gradient(ellipse at 80% 80%, rgba(5, 150, 105, 0.2) 0%, transparent 50%), radial-gradient(circle at 50% 50%, #051d16 0%, #020c09 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(5, 33, 24, 0.96) 0%, rgba(2, 12, 9, 0.98) 100%)",
        "card_bg": "linear-gradient(145deg, rgba(6, 78, 59, 0.6), rgba(3, 28, 20, 0.88))",
        "primary": "#34d399",
        "accent": "#10b981",
        "glow": "rgba(16, 185, 129, 0.4)",
        "border": "rgba(16, 185, 129, 0.3)",
        "badge_bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(5, 150, 105, 0.3))",
        "badge_color": "#6ee7b7"
    },
    "🔥 Dragon Crimson": {
        "name": "Dragon Crimson",
        "bg": "radial-gradient(ellipse at 20% 20%, rgba(239, 68, 68, 0.26) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(245, 158, 11, 0.22) 0%, transparent 50%), radial-gradient(circle at 50% 50%, #1f0808 0%, #0a0303 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(38, 11, 11, 0.96) 0%, rgba(10, 3, 3, 0.98) 100%)",
        "card_bg": "linear-gradient(145deg, rgba(69, 18, 18, 0.68), rgba(24, 7, 7, 0.88))",
        "primary": "#f87171",
        "accent": "#fbbf24",
        "glow": "rgba(239, 68, 68, 0.4)",
        "border": "rgba(239, 68, 68, 0.3)",
        "badge_bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(245, 158, 11, 0.3))",
        "badge_color": "#fca5a5"
    }
}

# ------------------------------------------------------------------------------
# 3. GAME CONSTANTS & MOVE DEFINITIONS
# ------------------------------------------------------------------------------
MOVES = {
    1: {"name": "Rock", "icon": "🪨", "sub": "Crushes Scissors ✂️", "beats": 3},
    2: {"name": "Paper", "icon": "📄", "sub": "Covers Rock 🪨", "beats": 1},
    3: {"name": "Scissors", "icon": "✂️", "sub": "Cuts Paper 📄", "beats": 2}
}

FLAVORS = {
    (1, 3): "🪨 Rock completely crushes ✂️ Scissors!",
    (2, 1): "📄 Paper cleanly envelopes 🪨 Rock!",
    (3, 2): "✂️ Scissors razor-shreds 📄 Paper!"
}

# ------------------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# ------------------------------------------------------------------------------
if "human_score" not in st.session_state:
    st.session_state.human_score = 0

if "comp_score" not in st.session_state:
    st.session_state.comp_score = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0

if "round_number" not in st.session_state:
    st.session_state.round_number = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "last_duel" not in st.session_state:
    st.session_state.last_duel = None

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "max_streak" not in st.session_state:
    st.session_state.max_streak = 0

if "user_move_frequencies" not in st.session_state:
    st.session_state.user_move_frequencies = {1: 0, 2: 0, 3: 0}

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "🌌 Cyber Cosmic"

if "celebration_triggered" not in st.session_state:
    st.session_state.celebration_triggered = False

def reset_game_state():
    """Wipes match session memory for a fresh game."""
    st.session_state.human_score = 0
    st.session_state.comp_score = 0
    st.session_state.draws = 0
    st.session_state.round_number = 0
    st.session_state.history = []
    st.session_state.last_duel = None
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.user_move_frequencies = {1: 0, 2: 0, 3: 0}
    st.session_state.celebration_triggered = False

# ------------------------------------------------------------------------------
# 5. SIDEBAR: MATCH SETTINGS, THEME SWITCHER & ANALYTICS
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎨 Visual Theme")
    theme_choice = st.selectbox(
        "Atmosphere & Aesthetics:",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.selected_theme)
        if st.session_state.selected_theme in THEMES else 0,
        help="Transforms background atmospheric gradients, card glows, and accents."
    )
    if theme_choice != st.session_state.selected_theme:
        st.session_state.selected_theme = theme_choice
        trigger_rerun()

    active_theme = THEMES[st.session_state.selected_theme]

    sound_enabled = st.checkbox("🔊 Celebration Audio Effects", value=True, help="Plays triumphant Web Audio chimes on win/loss.")

    st.markdown("---")
    st.markdown("### ⚙️ Combat Rules")

    target_score = st.selectbox(
        "🏆 Target Score (First to reach):",
        options=[3, 5, 7, 10],
        index=1,
        help="Match concludes when either contestant hits this threshold."
    )

    ai_mode = st.radio(
        "🧠 AI Combat Personality:",
        options=["Standard Bot (Fair Random)", "Psychic Bot (Adaptive AI)"],
        index=0,
        help="Psychic Bot studies your move patterns and attempts tactical counters."
    )

    st.markdown("---")

    # Match Statistics Hub
    st.markdown("### 📊 Combat Analytics")
    total_rounds = st.session_state.round_number
    win_rate = (
        round((st.session_state.human_score / total_rounds) * 100, 1)
        if total_rounds > 0 else 0.0
    )

    streak_emojis = "🔥 " * min(st.session_state.streak, 3)

    st.markdown(f"""
    <div class="stat-badge">
        <span class="stat-label">Total Rounds</span>
        <span class="stat-val">{total_rounds}</span>
    </div>
    <div class="stat-badge">
        <span class="stat-label">Player Win Rate</span>
        <span class="stat-val">{win_rate}%</span>
    </div>
    <div class="stat-badge">
        <span class="stat-label">Current Streak</span>
        <span class="stat-val">{streak_emojis}{st.session_state.streak}</span>
    </div>
    <div class="stat-badge">
        <span class="stat-label">Peak Streak</span>
        <span class="stat-val">⭐ {st.session_state.max_streak}</span>
    </div>
    <div class="stat-badge">
        <span class="stat-label">Stalemates (Draws)</span>
        <span class="stat-val">⚖️ {st.session_state.draws}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔄 Reset Match", use_container_width=True, help="Clear all scores and restart"):
        reset_game_state()
        trigger_rerun()

    # Move History Feed
    if st.session_state.history:
        st.markdown("### 📜 Battle Log (Recent)")
        for item in reversed(st.session_state.history[-6:]):
            badge_class = f"history-{item['outcome']}"
            outcome_symbol = "✅ Win" if item['outcome'] == "win" else ("❌ Loss" if item['outcome'] == "lose" else "⚖️ Draw")
            st.markdown(f"""
            <div class="history-card {badge_class}">
                <span><b>R{item['round']}:</b> {item['player_icon']} vs {item['comp_icon']}</span>
                <span>{outcome_symbol}</span>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("📖 Rules of Combat"):
        st.markdown("""
        - **🪨 Rock** beats **✂️ Scissors**
        - **📄 Paper** beats **🪨 Rock**
        - **✂️ Scissors** beats **📄 Paper**
        - Identical choices result in a **Draw**.
        - First to reach the **Target Score** wins the championship!
        """)

# ------------------------------------------------------------------------------
# 6. INJECT DYNAMIC THEMED CSS STYLES
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Dynamic Atmospheric Background */
    .stApp {{
        background: {active_theme['bg']} !important;
        background-attachment: fixed !important;
        color: #f8fafc;
    }}

    [data-testid="stSidebar"] {{
        background: {active_theme['sidebar_bg']} !important;
        border-right: 1px solid {active_theme['border']} !important;
    }}

    /* Container Spacing */
    .block-container {{
        padding-top: 1.6rem;
        padding-bottom: 3.2rem;
        max-width: 820px;
    }}

    /* Header Badge with Dynamic Pulse */
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 14px {active_theme['glow']}; }}
        50% {{ box-shadow: 0 0 28px {active_theme['glow']}; }}
    }}

    .arcade-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 15px;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: {active_theme['badge_bg']};
        border: 1px solid {active_theme['border']};
        color: {active_theme['badge_color']};
        border-radius: 9999px;
        margin-bottom: 0.7rem;
        animation: pulseGlow 3s infinite;
    }}

    /* Hero Header */
    .hero-title {{
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 40%, {active_theme['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        line-height: 1.15;
    }}

    .hero-subtitle {{
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.4rem;
    }}

    /* Scoreboard Card */
    .arena-scoreboard {{
        background: {active_theme['card_bg']};
        border: 1px solid {active_theme['border']};
        border-radius: 20px;
        padding: 1.2rem 1.4rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.55);
        margin-bottom: 1.4rem;
    }}

    .player-card {{
        text-align: center;
        padding: 0.6rem 0.4rem;
        border-radius: 14px;
    }}

    .player-avatar {{
        font-size: 2.5rem;
        line-height: 1;
        margin-bottom: 0.3rem;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.4));
    }}

    .player-name {{
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }}

    .player-human .player-name {{
        color: #38bdf8;
    }}

    .player-ai .player-name {{
        color: #f43f5e;
    }}

    .score-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.7rem;
        font-weight: 900;
        line-height: 1;
        margin: 0.35rem 0;
    }}

    .human-score-value {{
        color: #38bdf8;
        text-shadow: 0 0 25px rgba(56, 189, 248, 0.5);
    }}

    .ai-score-value {{
        color: #f43f5e;
        text-shadow: 0 0 25px rgba(244, 63, 94, 0.5);
    }}

    .vs-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding-top: 0.8rem;
    }}

    .vs-pill {{
        font-size: 1.05rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        padding: 6px 14px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #f1f5f9;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }}

    .round-tag {{
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 700;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }}

    /* Duel Arena Showcase */
    .battle-showcase {{
        background: {active_theme['card_bg']};
        border: 1px solid {active_theme['border']};
        border-radius: 20px;
        padding: 1.3rem;
        margin-bottom: 1.6rem;
        text-align: center;
        box-shadow: 0 14px 30px -8px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
    }}

    .clash-grid {{
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 16px;
        margin: 0.8rem 0;
    }}

    .move-box {{
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.1rem 0.6rem;
    }}

    .move-box-human {{
        border-bottom: 4px solid #38bdf8;
        box-shadow: 0 8px 20px -6px rgba(56, 189, 248, 0.3);
    }}

    .move-box-ai {{
        border-bottom: 4px solid #f43f5e;
        box-shadow: 0 8px 20px -6px rgba(244, 63, 94, 0.3);
    }}

    .move-box .icon {{
        font-size: 3rem;
        display: block;
        margin-bottom: 0.3rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }}

    .move-box .label {{
        font-size: 0.82rem;
        font-weight: 800;
        color: #f1f5f9;
        letter-spacing: 0.6px;
    }}

    .outcome-pill {{
        display: inline-block;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: 0.6px;
        padding: 7px 20px;
        border-radius: 9999px;
    }}

    .outcome-win {{
        background: rgba(34, 197, 94, 0.16);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.25);
    }}

    .outcome-lose {{
        background: rgba(239, 68, 68, 0.16);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.25);
    }}

    .outcome-draw {{
        background: rgba(234, 179, 8, 0.16);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.4);
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.25);
    }}

    .flavor-text {{
        font-size: 0.92rem;
        color: #cbd5e1;
        margin-top: 0.6rem;
        font-weight: 500;
    }}

    /* Action Deck */
    .deck-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.85rem;
        padding: 0 4px;
    }}

    .deck-title {{
        font-size: 0.95rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #cbd5e1;
    }}

    .deck-hint {{
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 500;
    }}

    /* Tactile Custom Button Styling */
    div[data-testid="stColumn"] > div > div.stButton > button {{
        width: 100% !important;
        border-radius: 16px !important;
        padding: 0.9rem 0.5rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: linear-gradient(145deg, #1e293b, #0f172a) !important;
        color: #f8fafc !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3) !important;
    }}

    div[data-testid="stColumn"] > div > div.stButton > button:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        border-color: {active_theme['accent']} !important;
        box-shadow: 0 12px 28px -4px {active_theme['glow']} !important;
        background: linear-gradient(145deg, #28374d, #141e30) !important;
    }}

    div[data-testid="stColumn"] > div > div.stButton > button:active {{
        transform: translateY(1px) scale(0.98) !important;
    }}

    .move-hint-text {{
        text-align: center;
        font-size: 0.74rem;
        color: #64748b;
        margin-top: 0.4rem;
        font-weight: 600;
    }}

    /* ========================================================================= */
    /* 👑 GRAND CHAMPIONSHIP CELEBRATION CARD                                     */
    /* ========================================================================= */
    @keyframes goldShimmer {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes floatCrown {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-8px) rotate(2deg); }}
    }}

    .championship-card {{
        border-radius: 26px;
        padding: 2.4rem 1.8rem;
        text-align: center;
        backdrop-filter: blur(24px);
        margin-bottom: 1.8rem;
        background: linear-gradient(145deg, rgba(251, 191, 36, 0.14) 0%, rgba(16, 185, 129, 0.12) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid rgba(251, 191, 36, 0.6);
        box-shadow: 0 25px 60px -15px rgba(251, 191, 36, 0.35);
    }}

    .defeat-card {{
        border-radius: 26px;
        padding: 2.4rem 1.8rem;
        text-align: center;
        backdrop-filter: blur(24px);
        margin-bottom: 1.8rem;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.16) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid rgba(248, 113, 113, 0.45);
        box-shadow: 0 25px 60px -15px rgba(239, 68, 68, 0.35);
    }}

    .champion-trophy {{
        font-size: 4.2rem;
        display: inline-block;
        margin-bottom: 0.3rem;
        animation: floatCrown 3s ease-in-out infinite;
        filter: drop-shadow(0 0 30px rgba(251, 191, 36, 0.7));
    }}

    .defeat-robot {{
        font-size: 4rem;
        display: inline-block;
        margin-bottom: 0.3rem;
        filter: drop-shadow(0 0 30px rgba(239, 68, 68, 0.6));
    }}

    .champion-title {{
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #ffe066, #f59e0b, #fffbeb, #fbbf24, #ffe066);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: goldShimmer 3s ease infinite;
        margin-bottom: 0.4rem;
    }}

    .defeat-title {{
        font-size: 2rem;
        font-weight: 900;
        color: #f87171;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }}

    .champion-tier-pill {{
        display: inline-block;
        padding: 5px 16px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        background: rgba(251, 191, 36, 0.18);
        border: 1px solid rgba(251, 191, 36, 0.5);
        color: #fde047;
        margin-bottom: 1.2rem;
    }}

    /* Championship 4-Pill Metric Grid */
    .champ-stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 1.2rem;
        margin-bottom: 1.4rem;
    }}

    .champ-stat-card {{
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 10px 6px;
        text-align: center;
    }}

    .champ-stat-card .label {{
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}

    .champ-stat-card .value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.2rem;
        font-weight: 800;
        color: #f8fafc;
    }}

    /* Sidebar Stat Chips */
    .stat-badge {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 9px 13px;
        margin-bottom: 8px;
    }}

    .stat-label {{
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 500;
    }}

    .stat-val {{
        font-size: 0.95rem;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* History Feed */
    .history-card {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.6);
        border-left: 3px solid #64748b;
        padding: 7px 11px;
        border-radius: 8px;
        margin-bottom: 6px;
        font-size: 0.8rem;
    }}
    .history-win {{ border-left-color: #22c55e; }}
    .history-lose {{ border-left-color: #ef4444; }}
    .history-draw {{ border-left-color: #eab308; }}

    @media (max-width: 600px) {{
        .champ-stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. CELEBRATION ENGINE (CONFETTI CANNONS & WEB AUDIO API)
# ------------------------------------------------------------------------------
def trigger_celebration(victory=True, play_audio=True):
    """Executes high-grade confetti starbursts and harmonious audio fanfares."""
    if victory:
        audio_script = """
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const chords = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6 (Triumphant fanfare)
                chords.forEach((freq, idx) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.16);
                    gain.gain.setValueAtTime(0.24, ctx.currentTime + idx * 0.16);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.16 + 0.55);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + idx * 0.16);
                    osc.stop(ctx.currentTime + idx * 0.16 + 0.6);
                });
            } catch(e) {}
        """ if play_audio else ""

        html_code = f"""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
        <script>
            // Mount full-screen canvas to parent document for total screen takeover
            let targetDoc = document;
            try {{
                if (window.parent && window.parent.document) {{
                    targetDoc = window.parent.document;
                }}
            }} catch(e) {{}}

            let cCanvas = targetDoc.getElementById('rps-confetti-canvas');
            if (!cCanvas) {{
                cCanvas = targetDoc.createElement('canvas');
                cCanvas.id = 'rps-confetti-canvas';
                cCanvas.style.position = 'fixed';
                cCanvas.style.top = '0px';
                cCanvas.style.left = '0px';
                cCanvas.style.width = '100vw';
                cCanvas.style.height = '100vh';
                cCanvas.style.zIndex = '9999999';
                cCanvas.style.pointerEvents = 'none';
                targetDoc.body.appendChild(cCanvas);
            }}

            const fireConfetti = confetti.create(cCanvas, {{ resize: true, useWorker: true }});

            // Multi-Stage Confetti Cannons from bottom corners
            var duration = 4.5 * 1000;
            var end = Date.now() + duration;

            (function frame() {{
                fireConfetti({{
                    particleCount: 7,
                    angle: 60,
                    spread: 65,
                    origin: {{ x: 0, y: 0.85 }},
                    colors: ['#fbbf24', '#f59e0b', '#38bdf8', '#c084fc', '#ec4899', '#22c55e']
                }});
                fireConfetti({{
                    particleCount: 7,
                    angle: 120,
                    spread: 65,
                    origin: {{ x: 1, y: 0.85 }},
                    colors: ['#fbbf24', '#f59e0b', '#38bdf8', '#c084fc', '#ec4899', '#22c55e']
                }});

                if (Date.now() < end) {{
                    requestAnimationFrame(frame);
                }}
            }}());

            // Center Golden Starburst Explosion
            setTimeout(function() {{
                fireConfetti({{
                    particleCount: 85,
                    spread: 120,
                    origin: {{ y: 0.45 }},
                    shapes: ['star', 'circle'],
                    colors: ['#FFE400', '#FFBD00', '#E89400', '#FFCA3A', '#ffffff']
                }});
            }}, 650);

            // Second Starburst Wave
            setTimeout(function() {{
                fireConfetti({{
                    particleCount: 50,
                    spread: 100,
                    origin: {{ y: 0.5 }},
                    shapes: ['star'],
                    colors: ['#f59e0b', '#ec4899', '#38bdf8']
                }});
            }}, 1400);

            {audio_script}
        </script>
        """
        components.html(html_code, height=0, width=0)
    else:
        audio_script = """
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const notes = [392.00, 369.99, 349.23, 311.13]; // Descending minor slide
                notes.forEach((freq, idx) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.18);
                    gain.gain.setValueAtTime(0.14, ctx.currentTime + idx * 0.18);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.18 + 0.4);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + idx * 0.18);
                    osc.stop(ctx.currentTime + idx * 0.18 + 0.45);
                });
            } catch(e) {}
        """ if play_audio else ""

        html_code = f"""
        <script>
            {audio_script}
        </script>
        """
        components.html(html_code, height=0, width=0)

# ------------------------------------------------------------------------------
# 8. HERO HEADER
# ------------------------------------------------------------------------------
st.markdown('<div class="arcade-badge">⚡ ARCADE DUEL ARENA • CHAMPIONSHIP</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Rock • Paper • Scissors</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-subtitle">First contender to achieve <b>{target_score} points</b> claims victory. Choose your weapon!</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# 9. GAME OVER CHECK & GRAND CHAMPION CELEBRATION
# ------------------------------------------------------------------------------
game_over = (st.session_state.human_score >= target_score) or (st.session_state.comp_score >= target_score)

if game_over:
    # Trigger victory/defeat celebration once upon match end (never re-fires on theme changes)
    if not st.session_state.celebration_triggered:
        trigger_celebration(victory=(st.session_state.human_score >= target_score), play_audio=sound_enabled)
        st.session_state.celebration_triggered = True

    if st.session_state.human_score >= target_score:
        # Calculate Honor Rank Tier
        win_pct = round((st.session_state.human_score / max(st.session_state.round_number, 1)) * 100, 1)
        if win_pct >= 90:
            honor_tier = "⚡ UNTOUCHABLE TITAN (Flawless)"
        elif win_pct >= 70:
            honor_tier = "🗡️ GRANDMASTER OF COMBAT"
        elif win_pct >= 50:
            honor_tier = "⚔️ SEASONED ARENA DUELIST"
        else:
            honor_tier = "🛡️ RESILIENT SURVIVOR"

        st.markdown(f"""
        <div class="championship-card">
            <div class="champion-trophy">🏆</div>
            <div class="champion-title">GRAND ARENA CHAMPION</div>
            <div class="champion-tier-pill">{honor_tier}</div>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0;">
                You conquered the championship tournament with decisive tactical mastery!
            </p>
            <div class="champ-stats-grid">
                <div class="champ-stat-card">
                    <div class="label">Final Score</div>
                    <div class="value" style="color: #4ade80;">{st.session_state.human_score} - {st.session_state.comp_score}</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">Win Rate</div>
                    <div class="value" style="color: #38bdf8;">{win_pct}%</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">Peak Streak</div>
                    <div class="value" style="color: #facc15;">⭐ {st.session_state.max_streak}</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">Rounds Fought</div>
                    <div class="value" style="color: #c084fc;">{st.session_state.round_number}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="defeat-card">
            <div class="defeat-robot">🤖</div>
            <div class="defeat-title">THE AI CLAIMED THE CROWN!</div>
            <div class="champion-tier-pill" style="border-color: rgba(239, 68, 68, 0.5); color: #fca5a5; background: rgba(239, 68, 68, 0.15);">
                TOURNAMENT DEFEAT
            </div>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0;">
                The machine seized the victory with a score of <b>{st.session_state.comp_score} - {st.session_state.human_score}</b>.
            </p>
            <div class="champ-stats-grid">
                <div class="champ-stat-card">
                    <div class="label">Final Score</div>
                    <div class="value" style="color: #f87171;">{st.session_state.comp_score} - {st.session_state.human_score}</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">AI Score</div>
                    <div class="value" style="color: #f87171;">{st.session_state.comp_score}</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">Your Score</div>
                    <div class="value" style="color: #38bdf8;">{st.session_state.human_score}</div>
                </div>
                <div class="champ-stat-card">
                    <div class="label">Rounds Fought</div>
                    <div class="value" style="color: #94a3b8;">{st.session_state.round_number}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    rematch_col1, rematch_col2, rematch_col3 = st.columns([1, 2, 1])
    with rematch_col2:
        if st.button("⚔️ Play Rematch", type="primary", use_container_width=True):
            reset_game_state()
            trigger_rerun()

    st.stop()

# ------------------------------------------------------------------------------
# 10. HEAD-TO-HEAD ARENA SCOREBOARD
# ------------------------------------------------------------------------------
score_col1, score_col2, score_col3 = st.columns([5, 2, 5])

human_progress = min(float(st.session_state.human_score) / float(target_score), 1.0)
comp_progress = min(float(st.session_state.comp_score) / float(target_score), 1.0)

with score_col1:
    st.markdown(f"""
    <div class="player-card player-human">
        <div class="player-avatar">👤</div>
        <div class="player-name">Player (You)</div>
        <div class="score-value human-score-value">{st.session_state.human_score}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(human_progress)

with score_col2:
    st.markdown(f"""
    <div class="vs-container">
        <div class="vs-pill">VS</div>
        <div class="round-tag">Round {st.session_state.round_number + 1}</div>
    </div>
    """, unsafe_allow_html=True)

with score_col3:
    st.markdown(f"""
    <div class="player-card player-ai">
        <div class="player-avatar">🤖</div>
        <div class="player-name">AI Contender</div>
        <div class="score-value ai-score-value">{st.session_state.comp_score}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(comp_progress)

# ------------------------------------------------------------------------------
# 11. ARENA DUEL SHOWCASE (LAST MOVE REVEAL)
# ------------------------------------------------------------------------------
if st.session_state.last_duel:
    duel = st.session_state.last_duel
    p_move = MOVES[duel["player"]]
    c_move = MOVES[duel["comp"]]

    if duel["outcome"] == "win":
        badge_html = '<span class="outcome-pill outcome-win">🎉 ROUND WON! (+1 POINT)</span>'
    elif duel["outcome"] == "lose":
        badge_html = '<span class="outcome-pill outcome-lose">❌ ROUND LOST!</span>'
    else:
        badge_html = '<span class="outcome-pill outcome-draw">⚖️ STALEMATE (DRAW)</span>'

    st.markdown(f"""
    <div class="battle-showcase">
        <div style="margin-bottom: 0.6rem;">{badge_html}</div>
        <div class="clash-grid">
            <div class="move-box move-box-human">
                <span class="icon">{p_move['icon']}</span>
                <span class="label">YOU PLAYED {p_move['name'].upper()}</span>
            </div>
            <div style="font-size: 1.5rem; font-weight: 900; color: #475569;">⚔️</div>
            <div class="move-box move-box-ai">
                <span class="icon">{c_move['icon']}</span>
                <span class="label">AI PLAYED {c_move['name'].upper()}</span>
            </div>
        </div>
        <div class="flavor-text">{duel['flavor']}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Introductory State
    st.markdown("""
    <div class="battle-showcase" style="padding: 1.6rem 1rem; border-style: dashed;">
        <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">⚔️</div>
        <div style="font-weight: 700; color: #f1f5f9; font-size: 1.05rem; margin-bottom: 0.2rem;">Arena Awaiting Contenders</div>
        <div style="color: #64748b; font-size: 0.88rem;">Select your opening weapon below to initiate Round 1.</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 12. GAME ENGINE (MOVE RESOLUTION)
# ------------------------------------------------------------------------------
def execute_round(player_choice: int):
    """Executes a round against the selected AI algorithm."""
    # AI Decision Engine
    if "Psychic" in ai_mode and st.session_state.round_number >= 2:
        # Predict human's next move based on their most frequent choice
        freqs = st.session_state.user_move_frequencies
        predicted_move = max(freqs, key=freqs.get)
        # Find counter move
        counter_move = [k for k, v in MOVES.items() if v["beats"] == predicted_move][0]
        # 60% probability of tactical counter-move, 40% random
        if random.random() < 0.60:
            comp_choice = counter_move
        else:
            comp_choice = random.randint(1, 3)
    else:
        comp_choice = random.randint(1, 3)

    # Track player movement patterns
    st.session_state.user_move_frequencies[player_choice] += 1
    st.session_state.round_number += 1

    # Evaluate Winner
    if player_choice == comp_choice:
        outcome = "draw"
        st.session_state.draws += 1
        flavor = "Twin strikes collide in a flurry of sparks! No score awarded."
    elif MOVES[player_choice]["beats"] == comp_choice:
        outcome = "win"
        st.session_state.human_score += 1
        st.session_state.streak += 1
        if st.session_state.streak > st.session_state.max_streak:
            st.session_state.max_streak = st.session_state.streak
        flavor = FLAVORS.get((player_choice, comp_choice), "A clean and decisive blow lands!")
    else:
        outcome = "lose"
        st.session_state.comp_score += 1
        st.session_state.streak = 0
        winning_flavor = FLAVORS.get((comp_choice, player_choice), "The AI deflects and scores a point!")
        flavor = f"AI's {winning_flavor}"

    # Save Last Duel Details
    st.session_state.last_duel = {
        "player": player_choice,
        "comp": comp_choice,
        "outcome": outcome,
        "flavor": flavor
    }

    # Record to History Log
    st.session_state.history.append({
        "round": st.session_state.round_number,
        "player_icon": MOVES[player_choice]["icon"],
        "comp_icon": MOVES[comp_choice]["icon"],
        "outcome": outcome
    })

    trigger_rerun()

# ------------------------------------------------------------------------------
# 13. ACTION DECK (TACTILE WEAPON SELECTOR)
# ------------------------------------------------------------------------------
st.markdown("""
<div class="deck-header">
    <span class="deck-title">Deploy Your Weapon</span>
    <span class="deck-hint">Click any weapon card to strike</span>
</div>
""", unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("🪨  ROCK", use_container_width=True, key="btn_rock"):
        execute_round(1)
    st.markdown('<div class="move-hint-text">Crushes Scissors ✂️</div>', unsafe_allow_html=True)

with btn_col2:
    if st.button("📄  PAPER", use_container_width=True, key="btn_paper"):
        execute_round(2)
    st.markdown('<div class="move-hint-text">Covers Rock 🪨</div>', unsafe_allow_html=True)

with btn_col3:
    if st.button("✂️  SCISSORS", use_container_width=True, key="btn_scissors"):
        execute_round(3)
    st.markdown('<div class="move-hint-text">Cuts Paper 📄</div>', unsafe_allow_html=True)
