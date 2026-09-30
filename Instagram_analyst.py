"""
Instagram Profile Analyst & Visualizer
Analyzes public Instagram profile statistics, calculates key metrics,
and generates structured reports and visualization charts.

Dependencies:
    pip install instaloader pandas matplotlib
"""

import os
import sys
import re
from typing import Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles to prevent UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Safe dependency imports with clear user-facing feedback
missing_deps = []

try:
    import instaloader
    from instaloader.exceptions import (
        ProfileNotExistsException,
        PrivateProfileNotFollowedException,
        LoginRequiredException,
        ConnectionException,
        BadCredentialsException,
        TwoFactorAuthRequiredException,
    )
except ImportError:
    missing_deps.append("instaloader")

try:
    import pandas as pd
except ImportError:
    missing_deps.append("pandas")

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    missing_deps.append("matplotlib")


def check_dependencies() -> bool:
    """Check if all required third-party libraries are installed."""
    if missing_deps:
        print("\n" + "=" * 60)
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\nPlease install them by running:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("=" * 60 + "\n")
        return False
    return True


def sanitize_username(raw_input: str) -> str:
    """
    Extract a clean username from input strings, handles with '@',
    or full Instagram URLs (e.g., https://www.instagram.com/cristiano/).
    """
    cleaned = raw_input.strip()

    # Extract username if a full Instagram URL was pasted
    if "instagram.com" in cleaned:
        match = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", cleaned)
        if match:
            return match.group(1).strip("/?#")

    # Remove leading '@', slashes, and trailing characters
    cleaned = cleaned.lstrip("@/").rstrip("/")
    return cleaned


def get_demo_profile() -> Dict[str, Any]:
    """Provide realistic sample profile data for instant testing and demonstration."""
    followers = 680_000_000
    following = 95
    posts = 7_450
    ratio = round(followers / max(1, following), 2)
    return {
        "username": "instagram",
        "full_name": "Instagram",
        "biography": "Discover what's next on Instagram ✨",
        "followers": followers,
        "following": following,
        "posts": posts,
        "is_verified": True,
        "is_private": False,
        "external_url": "https://about.instagram.com/",
        "ratio": ratio,
    }


def extract_profile_data(profile: Any) -> Dict[str, Any]:
    """Extract and structure relevant metrics from an Instaloader Profile object."""
    followers = getattr(profile, "followers", 0) or 0
    following = getattr(profile, "followees", 0) or 0
    posts = getattr(profile, "mediacount", 0) or 0
    ratio = round(followers / max(1, following), 2)

    return {
        "username": getattr(profile, "username", "Unknown"),
        "full_name": getattr(profile, "full_name", "") or "",
        "biography": getattr(profile, "biography", "") or "",
        "followers": followers,
        "following": following,
        "posts": posts,
        "is_verified": getattr(profile, "is_verified", False),
        "is_private": getattr(profile, "is_private", False),
        "external_url": getattr(profile, "external_url", "") or "",
        "ratio": ratio,
    }


def handle_login(loader: Any) -> bool:
    """Guide the user through optional login or loading a saved session."""
    print("\n" + "-" * 50)
    print("🔐 Instagram Authentication Options:")
    print("  [1] Log in with Instagram account (session will be saved locally)")
    print("  [2] Load existing session file")
    print("  [3] Continue without logging in")
    print("-" * 50)

    choice = input("👉 Select an option (1/2/3): ").strip()

    if choice == "1":
        login_user = input("Enter your Instagram username: ").strip().lstrip("@")
        try:
            loader.interactive_login(login_user)
            loader.save_session_to_file()
            print(f"✅ Successfully logged in as @{login_user} and saved session!")
            return True
        except BadCredentialsException:
            print("❌ Invalid username or password.")
        except TwoFactorAuthRequiredException:
            print("❌ Two-factor authentication required. Please login using the Instaloader CLI.")
        except Exception as err:
            print(f"❌ Login failed: {err}")
    elif choice == "2":
        session_user = input("Enter username of the saved session: ").strip().lstrip("@")
        try:
            loader.load_session_from_file(session_user)
            print(f"✅ Loaded saved session for @{session_user}!")
            return True
        except FileNotFoundError:
            print(f"❌ No saved session file found for @{session_user}.")
        except Exception as err:
            print(f"❌ Failed to load session: {err}")

    return False


def fetch_profile(loader: Any, username: str) -> Optional[Dict[str, Any]]:
    """
    Fetch profile metadata from Instagram with comprehensive exception handling
    and login fallback for anti-bot / rate-limiting protections.
    """
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return extract_profile_data(profile)

    except LoginRequiredException:
        print(f"\n⚠️ Instagram blocked anonymous scraping for '@{username}' (Login Required).")
        print("Instagram often requires authentication to access profile details.")
        if handle_login(loader):
            try:
                profile = instaloader.Profile.from_username(loader.context, username)
                return extract_profile_data(profile)
            except Exception as retry_err:
                print(f"❌ Failed to fetch profile after login: {retry_err}")
        return None

    except ProfileNotExistsException:
        print(f"\n❌ Error: Profile '@{username}' does not exist.")
        print("Please check the spelling and try again.")
        return None

    except PrivateProfileNotFollowedException:
        print(f"\n🔒 Profile '@{username}' is private.")
        print("Followers and detailed media are restricted unless the account is followed.")
        try:
            # Metadata might still be partially accessible
            profile = instaloader.Profile.from_username(loader.context, username)
            return extract_profile_data(profile)
        except Exception:
            return None

    except ConnectionException as conn_err:
        print(f"\n❌ Instagram Connection Error: {conn_err}")
        print("💡 Instagram may be rate-limiting your IP (HTTP 429). Please wait a few minutes or use a VPN.")
        return None

    except Exception as err:
        print(f"\n❌ An unexpected error occurred: {err}")
        return None


def display_analytics(data: Dict[str, Any]) -> Any:
    """Print a clean CLI summary and return a pandas DataFrame."""
    verified_str = "✅ Yes" if data.get("is_verified") else "❌ No"
    account_str = "🔒 Private" if data.get("is_private") else "🌐 Public"

    print("\n" + "=" * 60)
    print(f"📸 Instagram Profile: @{data['username']}")
    if data.get("full_name"):
        print(f"👤 Display Name:     {data['full_name']}")
    print(f"🌟 Verified:         {verified_str}  |  Account: {account_str}")
    if data.get("biography"):
        bio_preview = data["biography"].replace("\n", " ").strip()
        if len(bio_preview) > 80:
            bio_preview = bio_preview[:77] + "..."
        print(f"📝 Bio:              {bio_preview}")
    if data.get("external_url"):
        print(f"🔗 Website:          {data['external_url']}")
    print("-" * 60)

    # Build DataFrame
    df = pd.DataFrame([
        {"Metric": "Followers", "Value": data["followers"], "Formatted": f"{data['followers']:,}"},
        {"Metric": "Following", "Value": data["following"], "Formatted": f"{data['following']:,}"},
        {"Metric": "Posts", "Value": data["posts"], "Formatted": f"{data['posts']:,}"},
    ])

    print("📊 Core Metrics:")
    for _, row in df.iterrows():
        print(f"   • {row['Metric']:<14}: {row['Formatted']:>15}")

    print(f"   • {'F/F Ratio':<14}: {data['ratio']:>14,.2f}x")
    print("=" * 60 + "\n")

    return df


def plot_analytics(data: Dict[str, Any], save_filename: Optional[str] = None):
    """
    Generate a modern, visually striking 2-panel Instagram analytics dashboard.
    Left panel: Audience size (Followers)
    Right panel: Activity & Network (Following vs Posts)
    This dual-panel design prevents the massive scale difference of Followers
    from dwarfing Following and Posts into invisible flat bars.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={"width_ratios": [1, 1.4]})
    fig.patch.set_facecolor("#FAFAFA")

    # Helper for nice axis number abbreviations (e.g., 10K, 1.5M)
    def count_formatter(val, _):
        if val >= 1_000_000:
            return f"{val * 1e-6:.1f}M"
        if val >= 1_000:
            return f"{val * 1e-3:.1f}K"
        return f"{int(val)}"

    formatter = ticker.FuncFormatter(count_formatter)

    # Left Panel: Followers
    ax1.set_facecolor("#FFFFFF")
    bar1 = ax1.bar(["Followers"], [data["followers"]], color="#833AB4", width=0.45, edgecolor="#5B247A", linewidth=1.5)
    ax1.set_title("Audience Reach", fontsize=13, fontweight="bold", pad=12, color="#262626")
    ax1.set_ylabel("Total Count", fontsize=10, color="#555555")
    ax1.yaxis.set_major_formatter(formatter)
    ax1.grid(axis="y", linestyle="--", alpha=0.4, color="#C0C0C0")
    ax1.set_axisbelow(True)

    # Value label on top of bar
    ax1.bar_label(bar1, fmt=lambda x: f"{int(x):,}", fontsize=11, fontweight="bold", padding=4, color="#262626")

    # Right Panel: Following & Posts
    ax2.set_facecolor("#FFFFFF")
    metrics2 = ["Following", "Posts"]
    values2 = [data["following"], data["posts"]]
    colors2 = ["#E1306C", "#F77737"]
    edgecolors2 = ["#B2164A", "#C9551E"]

    bars2 = ax2.bar(metrics2, values2, color=colors2, width=0.48, edgecolor=edgecolors2, linewidth=1.5)
    ax2.set_title("Activity & Following", fontsize=13, fontweight="bold", pad=12, color="#262626")
    ax2.yaxis.set_major_formatter(formatter)
    ax2.grid(axis="y", linestyle="--", alpha=0.4, color="#C0C0C0")
    ax2.set_axisbelow(True)

    # Value labels on top of bars
    ax2.bar_label(bars2, fmt=lambda x: f"{int(x):,}", fontsize=11, fontweight="bold", padding=4, color="#262626")

    # Adjust y-limit headroom so labels don't get clipped
    for ax in (ax1, ax2):
        ylim = ax.get_ylim()
        ax.set_ylim(0, max(ylim[1] * 1.15, 1))

    # Supertitle & Subtitle
    display_title = data.get("full_name") or f"@{data['username']}"
    fig.suptitle(f"{display_title} (@{data['username']}) — Analytics", fontsize=16, fontweight="bold", y=0.98, color="#1A1A1A")

    verified_text = "Verified ✔" if data.get("is_verified") else "Unverified"
    privacy_text = "Private 🔒" if data.get("is_private") else "Public 🌐"
    sub_text = f"Follower/Following Ratio: {data['ratio']:,.2f}x  •  {verified_text}  •  {privacy_text}"
    fig.text(0.5, 0.91, sub_text, ha="center", fontsize=10.5, color="#666666")

    plt.subplots_adjust(top=0.84, bottom=0.12, wspace=0.3)

    if save_filename:
        try:
            fig.savefig(save_filename, dpi=150, bbox_inches="tight")
            print(f"📈 Chart successfully saved to: {save_filename}")
        except Exception as save_err:
            print(f"⚠️ Could not save chart image: {save_err}")

    try:
        plt.show()
    except Exception as show_err:
        print(f"ℹ️ Note: Displaying plot window failed ({show_err}). Chart saved to file.")
    finally:
        plt.close(fig)


def main():
    print("=" * 60)
    print("       📸 INSTAGRAM PROFILE ANALYST & VISUALIZER 📊       ")
    print("=" * 60)

    if not check_dependencies():
        return

    try:
        raw_input_user = input("\n👉 Enter Instagram username or URL (or 'demo' for sample): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Operation cancelled. Goodbye!")
        return

    if not raw_input_user:
        print("❌ Username cannot be empty. Exiting.")
        return

    target_user = sanitize_username(raw_input_user)

    # Allow testing without network or login
    if target_user.lower() == "demo":
        print("\n✨ Loading sample demonstration data...")
        data = get_demo_profile()
    else:
        print(f"\n🔍 Connecting to Instagram to analyze @{target_user}...")
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
        )
        data = fetch_profile(loader, target_user)

    if not data:
        try:
            demo_choice = input("\n👉 Would you like to view a sample demo analytics chart instead? (y/n): ").strip().lower()
            if demo_choice == "y":
                data = get_demo_profile()
            else:
                print("Exiting.")
                return
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return

    # Print summary and create DataFrame
    df = display_analytics(data)

    # Optional CSV Export
    try:
        export_csv = input("👉 Export metrics to CSV? (y/n): ").strip().lower()
        if export_csv == "y":
            csv_filename = f"{data['username']}_analytics.csv"
            df.to_csv(csv_filename, index=False)
            print(f"💾 Data saved to: {csv_filename}")
    except (KeyboardInterrupt, EOFError):
        pass

    # Generate and display plot
    chart_filename = f"{data['username']}_analytics.png"
    print("\n📊 Generating analytics visualization...")
    plot_analytics(data, save_filename=chart_filename)

    print("\n🎉 Analysis complete!\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Process terminated by user.")