import instaloader
import pandas as pd
import matplotlib.pyplot as plt

l = instaloader.Instaloader()

username = input("Enter your Instagram username: ")

try:
    profile = instaloader.Profile.from_username(l.context, username)

    data = {
        "Followers": profile.followers,
        "Following": profile.followees,
        "Posts": profile.mediacount
    }

    df = pd.DataFrame(data.items(), columns=['Metric', 'Value'])

    print("\nInstagram Analytics")
    print(df)

    plt.figure(figsize=(6, 4))
    plt.bar(df['Metric'], df['Value'])
    plt.title(f"{username} Analytics")
    plt.ylabel("Count")
    plt.show()

except Exception as e:
    print("Error:", e)