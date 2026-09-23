
# ---------- Calculator ----------

operations = {
    1: ("Addition", lambda a, b: a + b),
    2: ("Subtraction", lambda a, b: a - b),
    3: ("Multiplication", lambda a, b: a * b),
    4: ("Division", lambda a, b: a / b),
    5: ("Power", lambda a, b: a ** b),
    6: ("Floor Division", lambda a, b: a // b),
    7: ("Modulus", lambda a, b: a % b)
}

try:
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    print("\nChoose your operation:")
    for key, (name, _) in operations.items():
        print(f"{key} - {name}")

    choice = int(input("Enter choice (1-7): "))

    if choice not in operations:
        print("Invalid choice! Please select 1-7.")

    elif choice in (4, 6, 7) and b == 0:
        print("Error: Cannot divide by zero.")

    else:
        name, calculate = operations[choice]
        result = calculate(a, b)
        print(f"{name}: {result}")

except ValueError:
    print("Invalid input! Please enter valid numbers.")
except OverflowError:
    print("Error: The result is too large.")