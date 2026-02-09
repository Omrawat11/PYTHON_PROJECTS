import streamlit as st

# ---------------- DATA ----------------
questions = [
    "How many elements are there in the periodic table?",
    "Which animal lays the largest eggs?",
    "What is the most abundant gas in Earth's atmosphere?",
    "How many bones are there in the human body?",
    "Which planet in the solar system is the hottest?"
]

options = [
    ["117", "118", "119", "120"],
    ["Whale", "Crocodile", "Elephant", "Ostrich"],
    ["Nitrogen", "Oxygen", "Carbon Dioxide", "Hydrogen"],
    ["206", "207", "208", "209"],
    ["Mercury", "Venus", "Earth", "Mars"]
]

answers = ["118", "Ostrich", "Nitrogen", "206", "Venus"]

# ---------------- SESSION STATE ----------------
if "question_num" not in st.session_state:
    st.session_state.question_num = 0
    st.session_state.user_answers = [None] * len(questions)

# ---------------- UI ----------------
st.set_page_config(page_title="Quiz Game", page_icon="🧠")
st.title("🧠 Quiz Game")
st.write("You can move back and change your answers before submitting.")

# ---------------- PROGRESS BAR ----------------
progress_value = st.session_state.question_num / len(questions)
st.progress(min(progress_value, 1.0))

# ---------------- RESULT SCREEN ----------------
if st.session_state.question_num == len(questions):
    st.subheader("🎉 Quiz Finished!")

    score = 0
    for i in range(len(questions)):
        if st.session_state.user_answers[i] == answers[i]:
            score += 1

    percentage = int((score / len(questions)) * 100)

    st.write(f"**Your Score:** {score}/{len(questions)}")
    st.write(f"**Percentage:** {percentage}%")

    # 🎈 BALLOONS FOR FULL SCORE
    if score == len(questions):
        st.success("Perfect score! 🎯 All answers are correct!")
        st.balloons()
    elif percentage >= 80:
        st.success("Excellent performance 🌟")
    elif percentage >= 50:
        st.info("Good job 👍")
    else:
        st.warning("Keep practicing 💪")

    if st.button("Restart Quiz"):
        st.session_state.question_num = 0
        st.session_state.user_answers = [None] * len(questions)
        st.rerun()

# ---------------- QUESTION SCREEN ----------------
else:
    qn = st.session_state.question_num

    st.subheader(f"Question {qn + 1}")
    st.write(questions[qn])

    selected = st.radio(
        "Choose your answer:",
        options[qn],
        index=options[qn].index(st.session_state.user_answers[qn])
        if st.session_state.user_answers[qn] in options[qn]
        else 0,
        key=f"q_{qn}"
    )

    st.session_state.user_answers[qn] = selected

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back") and qn > 0:
            st.session_state.question_num -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡️"):
            st.session_state.question_num += 1
            st.rerun()
