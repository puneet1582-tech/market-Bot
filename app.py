import tkinter as tk
import subprocess

def run_bot():
    output = subprocess.getoutput("python3 main.py")
    text.delete(1.0, tk.END)
    text.insert(tk.END, output)

root = tk.Tk()
root.title("Market Intelligence App")

btn = tk.Button(root, text="RUN MARKET ANALYSIS", command=run_bot, 
font=("Arial", 14))
btn.pack(pady=10)

text = tk.Text(root, height=40, width=120)
text.pack()

root.mainloop()

