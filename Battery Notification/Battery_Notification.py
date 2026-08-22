# pip install psutil win10toast

import psutil
import time
from datetime import datetime
from win10toast import ToastNotifier

toaster = ToastNotifier()

LOW_BATTERY_THRESHOLD = 30      # percent
CRITICAL_BATTERY_THRESHOLD = 15 # percent
CHECK_INTERVAL = 60             # seconds

def get_time_remaining(battery):
    """Convert seconds left into readable HH:MM format."""
    secs = battery.secsleft
    if secs == psutil.POWER_TIME_UNLIMITED:
        return "Unlimited (plugged in)"
    elif secs == psutil.POWER_TIME_UNKNOWN:
        return "Calculating..."
    else:
        hours, remainder = divmod(secs, 3600)
        minutes = remainder // 60
        return f"{int(hours)}h {int(minutes)}m remaining"

def check_battery():
    battery = psutil.sensors_battery()

    if battery is None:
        print("No battery detected (desktop system?). Exiting monitor.")
        return False  # signal to stop the loop

    percent = battery.percent
    plugged = battery.power_plugged
    status = "Charging ⚡" if plugged else "On Battery 🔋"
    time_left = get_time_remaining(battery)
    now = datetime.now().strftime("%H:%M:%S")

    # Always show current status on console
    print(f"[{now}] Battery: {percent}% | {status} | {time_left}")

    if not plugged:
        if percent <= CRITICAL_BATTERY_THRESHOLD:
            toaster.show_toast(
                "⚠️ Critical Battery!",
                f"{percent}% remaining. Plug in now! ({time_left})",
                duration=8,
                threaded=True
            )
        elif percent <= LOW_BATTERY_THRESHOLD:
            toaster.show_toast(
                "Battery Low",
                f"{percent}% remaining. ({time_left})",
                duration=5,
                threaded=True
            )
    return True

def main():
    print("Battery monitor started. Press Ctrl+C to stop.\n")
    try:
        while True:
            if not check_battery():
                break
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nBattery monitor stopped.")

if __name__ == "__main__":
    main()