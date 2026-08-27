import calendar 
from datetime import  datetime

today = datetime.today()
year = int(input("Enter Year : "))
month = int(input("Enter Month (1-12): "))

cal = calendar.TextCalendar(calendar.SUNDAY)
lines = cal.formatmonth(year, month).splitlines()

if year == today.year and month == today.month:
    new_lines = []
    for line in lines:
        if str(today.day) in line.split():
            line = line.replace(f"{today.day:2d}", f"[{today.day}]")
            new_lines.append(line)

    print("\n".join(new_lines))
else:
    print(calendar.month(year, month))

 