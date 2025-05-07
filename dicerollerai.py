import tkinter as tk
import random
from tkinter import ttk

history_listbox = None  # Define at top level

def animate_dice_roll(times=10):
    if times > 0:
        dice_icon_label.config(text=random.choice(list(dice_faces.values())))
        root.after(100, lambda: animate_dice_roll(times - 1))
    else:
        show_result()

def roll_dice():
    try:
        int(user_guess.get())  # Validate guess
    except ValueError:
        dice_result_label.config(text="Please enter a valid guess!", fg="#E74C3C")
        return

    roll_button.config(state=tk.DISABLED)
    dice_result_label.config(text="Rolling...", font=("Arial", 20, "bold"), fg=text_color)
    animate_dice_roll()

def show_result():
    num_dice = int(selected_dice.get())
    dice_values = [random.randint(1, 6) for _ in range(num_dice)]
    total_value = sum(dice_values)
    dice_text = " ".join(dice_faces.get(value, str(value)) for value in dice_values)

    dice_icon_label.config(text=dice_text, font=("Arial", 60, "bold"), fg=random.choice(colors))
    dice_result_label.config(text=f"Dice Result: {', '.join(map(str, dice_values))}\nTotal: {total_value}", font=("Arial", 20, "bold"), fg=text_color)

    try:
        guess = int(user_guess.get())
        if guess == total_value:
            result_message = "🎉 Correct Guess!"
        else:
            result_message = f"❌ Incorrect. You guessed {guess}."
        dice_result_label.config(text=f"{dice_result_label.cget('text')}\n{result_message}")
    except ValueError:
        dice_result_label.config(text=f"{dice_result_label.cget('text')}\n(Invalid guess)")

    roll_button.config(state=tk.NORMAL)
    dice_history.append(", ".join(map(str, dice_values)))
    if len(dice_history) > 10:
        dice_history.pop(0)
    update_history_listbox()

def update_history_listbox():
    if history_listbox is None:
        return
    history_listbox.delete(0, tk.END)
    for entry in dice_history:
        history_listbox.insert(tk.END, entry)

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Dice History")
    history_window.geometry("300x200")
    history_window.configure(bg=bg_color)
    history_label = tk.Label(history_window, text="Dice Roll History", font=("Arial", 16, "bold"), bg=bg_color, fg=text_color)
    history_label.pack(pady=10)
    global history_listbox
    history_listbox = tk.Listbox(history_window, font=("Arial", 14), height=5, bg=bg_color, fg=text_color)
    history_listbox.pack(pady=10, fill="both", expand=True)
    update_history_listbox()

def toggle_theme():
    global bg_color, text_color
    with open("theme.txt", "w") as theme_file:
        theme_file.write(theme_var.get())
    if theme_var.get() == "Dark":
        bg_color = "#2C3E50"
        text_color = "#ECF0F1"
        theme_icon.config(text="🌙")
        style.configure("Custom.TButton", background="#E74C3C", foreground="black")
    else:
        bg_color = "#ECF0F1"
        text_color = "#000000"
        theme_icon.config(text="🌞")
        style.configure("Custom.TButton", background="#3498DB", foreground="black")

    root.configure(bg=bg_color)
    main_frame.config(bg=bg_color)
    theme_frame.config(bg=bg_color)
    for widget in root.winfo_children() + main_frame.winfo_children() + theme_frame.winfo_children():
        if isinstance(widget, (tk.Label, tk.Listbox, ttk.Radiobutton)):
            widget.config(bg=bg_color, fg=text_color)
        elif isinstance(widget, ttk.Button):
            widget.config(style="Custom.TButton")

root = tk.Tk()
root.title("🎲 AI Dice Roller")
root.geometry("500x750")
root.resizable(True, True)

bg_color = "#2C3E50"
text_color = "#ECF0F1"
root.configure(bg=bg_color)

style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 14, "bold"), padding=10)

colors = ["#FF5733", "#33FF57", "#3357FF", "#FFD700", "#FF69B4", "#8A2BE2"]
dice_faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

dice_history = []

main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

title_label = tk.Label(main_frame, text="🎲 AI Dice Roller", font=("Arial", 22, "bold"), bg=bg_color, fg=text_color)
title_label.pack(pady=15)

dice_icon_label = tk.Label(main_frame, text="🎲", font=("Arial", 60, "bold"), bg=bg_color, fg=random.choice(colors))
dice_icon_label.pack(pady=10)

dice_result_label = tk.Label(main_frame, text="", font=("Arial", 20, "bold"), bg=bg_color, fg=text_color)
dice_result_label.pack(pady=5)

selected_dice = tk.StringVar(value="1")
dice_spinbox = ttk.Spinbox(main_frame, textvariable=selected_dice, from_=1, to=6, wrap=True, width=5, font=("Arial", 14))
dice_spinbox.pack(pady=5)

# NEW: Guess Input
guess_label = tk.Label(main_frame, text="Your Guess (Total Value):", font=("Arial", 14), bg=bg_color, fg=text_color)
guess_label.pack(pady=5)

user_guess = tk.StringVar()
guess_entry = ttk.Entry(main_frame, textvariable=user_guess, font=("Arial", 14))
guess_entry.pack(pady=5)

roll_button = ttk.Button(main_frame, text="Roll Dice", command=roll_dice, style="Custom.TButton")
roll_button.pack(pady=10)

history_button = ttk.Button(main_frame, text="Show History", command=show_history, style="Custom.TButton")
history_button.pack(pady=5)

theme_var = tk.StringVar(value="Dark")
theme_frame = tk.Frame(main_frame, bg=bg_color)
theme_frame.pack(pady=10)

theme_icon = tk.Label(theme_frame, text="🌙", font=("Arial", 24), bg=bg_color, fg=text_color)
theme_icon.pack(side="left", padx=10)

theme_light_button = ttk.Radiobutton(theme_frame, text="Light", variable=theme_var, value="Light", command=toggle_theme)
theme_light_button.pack(side="left", padx=10)

theme_dark_button = ttk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value="Dark", command=toggle_theme)
theme_dark_button.pack(side="left", padx=10)

exit_button = ttk.Button(main_frame, text="Exit", command=root.quit, style="Custom.TButton")
exit_button.pack(pady=5)

root.mainloop()