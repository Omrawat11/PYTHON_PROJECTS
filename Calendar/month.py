from colorama import Fore, Style, init
import calendar

print("*" *30)
print("     PYTHON CALENDAR")
print("*" *30)

init()

year = int(input("Year: "))
month = int(input("Month: "))

print(Fore.CYAN)
print(calendar.month(year, month))
print(Style.RESET_ALL)