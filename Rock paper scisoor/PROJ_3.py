import streamlit as st
import random

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🎮",
    layout="centered"
)

# ------------------ Initialize Session State ------------------
if "human_score" not in st.session_state:
    st.session_state.human_score = 0

if "comp_score" not in st.session_state:
    st.session_state.comp_score = 0

if "result" not in st.session_state:
    st.session_state.result = ""

choices = {
    1: "🪨 Rock",
    2: "📄 Paper",
    3: "✂️ Scissors"
}

# ------------------ Title ------------------
st.title("🎮 Rock Paper Scissors Game")
st.subheader("🏆 First to score 5 points wins!")

# ------------------ Game Over Check ------------------
if st.session_state.human_score == 5:
    st.success("🎉🎉 CONGRATULATIONS! YOU WON THE GAME 🎉🎉")
    if st.button("🔄 Play Again"):
        st.session_state.human_score = 0
        st.session_state.comp_score = 0
        st.session_state.result = ""
    st.stop()

if st.session_state.comp_score == 5:
    st.error("🤖💥 COMPUTER WON THE GAME! TRY AGAIN 💥🤖")
    if st.button("🔄 Play Again"):
        st.session_state.human_score = 0
        st.session_state.comp_score = 0
        st.session_state.result = ""
    st.stop()

# ------------------ User Choice Buttons ------------------
st.write("### Choose your move:")

col1, col2, col3 = st.columns(3)

def play(you):
    comp = random.randint(1, 3)

    if (you == 1 and comp == 3) or (you == 2 and comp == 1) or (you == 3 and comp == 2):
        st.session_state.human_score += 1
        result = "✅ You WON this round! 🎉"
    elif you == comp:
        result = "⚖️ It's a DRAW!"
    else:
        st.session_state.comp_score += 1
        result = "❌ Computer WON this round! 🤖"

    st.session_state.result = f"""
👤 You chose: {choices[you]}  
🤖 Computer chose: {choices[comp]}  

{result}
"""

with col1:
    if st.button("🪨 Rock"):
        play(1)

with col2:
    if st.button("📄 Paper"):
        play(2)

with col3:
    if st.button("✂️ Scissors"):
        play(3)

# ------------------ Result & Score ------------------
st.markdown(st.session_state.result)

st.info(
    f"📊 **Current Score** → You: {st.session_state.human_score} | Computer: {st.session_state.comp_score}"
)
