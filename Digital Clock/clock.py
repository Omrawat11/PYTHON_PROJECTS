import tkinter as tk 
from time import strftime

# Create Window 
root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x150")
root.configure(bg="black")

# Function to update time 
def update_time():
    current_time = strftime("%H:%M:%S %p")
    time_label.config(text=current_time)
    time_label.after(1000, update_time)


# Clock label 
time_label = tk.Label(
    root,
    font=("Arial",40,"bold"),
    background='black',
    foreground='white'
)

time_label.pack(anchor='center')

# Start clock
update_time()

# Run Application
root.mainloop()