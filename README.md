# 🎯 Guess The Number – Car Race Edition (UI Explanation)

This document explains the **User Interface (UI)** and user interaction flow of the *Guess The Number – Car Race Edition* Streamlit application. It is intended to help reviewers, teachers, and collaborators understand how the UI behaves and how users interact with the app.

---

## 🖥️ Application Overview

The application is a web-based interactive game built using **Streamlit**. Users guess a randomly generated number within a limited number of attempts. The UI is designed to be simple, engaging, and beginner-friendly, with visual feedback and animations.

---

## 🎚️ Difficulty Selection (Top Section)

At the top of the UI, the user selects a difficulty level using a dropdown menu:

* **Easy** → Number range: 1–50, Attempts: 10
* **Medium** → Number range: 1–100, Attempts: 7
* **Hard** → Number range: 1–500, Attempts: 5

📌 The difficulty level directly affects the game logic and the UI messages shown to the user.

---

## 🧠 Game Instructions Display

Once a difficulty is selected, the UI displays:

* The valid number range for guessing
* The number of attempts remaining

This information updates dynamically as the user plays the game.

---

## 🔢 User Input Section

* A **number input box** allows the user to enter their guess.
* The input is restricted to valid values based on the selected difficulty.
* This prevents invalid or out-of-range guesses and improves user experience.

---

## 🔘 Submit Guess Button

* The **Submit Guess** button processes the user’s input.
* On each click:

  * The attempt counter increases
  * The app evaluates the guess

### UI Feedback Provided:

* ⬆️ *Go higher* → if the guess is too low
* ⬇️ *Go lower* → if the guess is too high
* 🎉 *Success message* → if the guess is correct
* 😢 *Failure message* → if attempts are exhausted

All feedback is shown using Streamlit alert components for clarity.

---

## 🚗 Winning Animation (Car Race)

When the user wins:

* A **progress bar animation** is displayed
* It visually represents a **car racing toward the finish line**
* The animation runs smoothly from 0% to 100%

🏁 This animation provides visual satisfaction and makes the win moment engaging.

---

## 🏆 Score Display

After the car animation completes:

* A score is calculated based on the number of attempts used
* The score is displayed clearly on the UI

This encourages users to win the game in fewer attempts.

---

## 🔄 Restart Game Button

* A **Restart Game** button is available at the bottom
* When clicked:

  * All session data is cleared
  * The app restarts without refreshing the browser

This allows users to replay the game smoothly.

---

## 🎨 UI Design Highlights

* Clean and minimal layout
* Emoji-based visual cues for engagement
* Real-time UI updates using Streamlit session state
* Beginner-friendly and responsive design

---

## 📌 Summary

The UI of this application focuses on:

* Simplicity
* Clear user guidance
* Interactive feedback
* Visual reward through animation

This makes the project suitable for **college submissions**, **GitHub portfolios**, and **LinkedIn showcases**.

---

✅ *End of UI Explanation*
