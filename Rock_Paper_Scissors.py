
import random

comp_score = 0
human_score = 0

choices = {
    1: "🪨 Rock",
    2: "📄 Paper",
    3: "✂️ Scissors"
}

print("🎮 Welcome to Rock Paper Scissors Game 🎮")
print("🏆 First to score 5 points wins!\n")

while True:
    if human_score == 5:
        print("\n🎉🎉 CONGRATULATIONS! YOU WON THE GAME 🎉🎉")
        break

    if comp_score == 5:
        print("\n🤖💥 COMPUTER WON THE GAME! TRY AGAIN 💥🤖")
        break

    print("\nChoose your move:")
    print("1️⃣ Rock 🪨")
    print("2️⃣ Paper 📄")
    print("3️⃣ Scissors ✂️")

    you = int(input("👉 Enter your choice (1/2/3): "))

    if you < 1 or you > 3:
        print("❌ Invalid choice! Please choose 1, 2 or 3.")
        continue

    comp = random.randint(1, 3)

    print(f"\n👤 You chose: {choices[you]}")
    print(f"🤖 Computer chose: {choices[comp]}")

    if (you == 1 and comp == 3) or (you == 2 and comp == 1) or (you == 3 and comp == 2):
        human_score += 1
        print("✅ You WON this round! 🎉")

    elif you == comp:
        print("⚖️ It's a DRAW!")

    else:
        comp_score += 1
        print("❌ Computer WON this round! 🤖")

    print(f"📊 Current Score → You: {human_score} | Computer: {comp_score}") 
