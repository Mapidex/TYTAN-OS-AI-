import tkinter as tk
from tkinter import scrolledtext, ttk
import g4f

# Ustawienia dostawcy g4f
provider = g4f.Provider.Free2GPT

# Lista modeli
models = {
    "T-ai 1 (BETA)": "gpt-3.5-turbo",
    "T-ai 2": "gpt-4",
    "T-ai 3 (K1)": "gpt-4-turbo"
}

# Tworzenie GUI
root = tk.Tk()
root.title("T-ai (∆1 beta)")
root.geometry("400x500")
root.configure(bg="#2C2F33")

# Pole czatu
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#23272A", fg="white", font=("Arial", 12))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_history.tag_config("user", foreground="cyan")
chat_history.tag_config("bot", foreground="lightgreen")
chat_history.tag_config("error", foreground="red")

# Wybór modelu
selected_model = tk.StringVar(value=list(models.keys())[0])
model_label = tk.Label(root, text="Wybierz model:", bg="#2C2F33", fg="white", font=("Arial", 10))
model_label.pack(pady=(5, 0))
model_dropdown = ttk.Combobox(root, textvariable=selected_model, values=list(models.keys()), state="readonly")
model_dropdown.pack(pady=5)

# Pole wpisywania wiadomości
entry = tk.Entry(root, font=("Arial", 12), bg="#99AAB5", fg="black")
entry.pack(padx=10, pady=5, fill=tk.X)

def send_message(event=None):  # Obsługa ENTER
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_history.insert(tk.END, f"Ty: {user_input}\n", "user")
    entry.delete(0, tk.END)
    chat_history.yview(tk.END)  # Automatyczne przewijanie

    if user_input == "T--ai--version":
        response = "To jest AI TytanKomp"
    else:
        try:
            response = g4f.ChatCompletion.create(
                model=models[selected_model.get()],
                provider=provider,
                messages=[{"role": "user", "content": user_input}]
            )
        except Exception as e:
            response = f"Błąd: {str(e)}"

    chat_history.insert(tk.END, f"T-ai: {response}\n", "bot")
    chat_history.yview(tk.END)

# Przycisk wysyłania
send_button = tk.Button(root, text="Wyślij", command=send_message, font=("Arial", 12), bg="#7289DA", fg="white")
send_button.pack(pady=5)

# Obsługa ENTER do wysyłania wiadomości
entry.bind("<Return>", send_message)

root.mainloop()
