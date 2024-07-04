import tkinter as tk
from tkinter import scrolledtext, messagebox
import difflib

class DiffCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diff Checker")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Original Text
        self.original_label = tk.Label(self.root, text="Original Text")
        self.original_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.original_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.original_text.grid(row=1, column=0, padx=10, pady=10)
        
        # Changed Text
        self.changed_label = tk.Label(self.root, text="Changed Text")
        self.changed_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.changed_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.changed_text.grid(row=1, column=1, padx=10, pady=10)
        
        # Compare Button
        self.compare_button = tk.Button(self.root, text="Compare", command=self.compare_texts)
        self.compare_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result Text
        self.result_label = tk.Label(self.root, text="Result")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=15)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # Merge Button
        self.merge_button = tk.Button(self.root, text="Merge Changes", command=self.merge_changes)
        self.merge_button.grid(row=5, column=0, columnspan=2, pady=10)
        
    def compare_texts(self):
        original = self.original_text.get("1.0", tk.END).splitlines()
        changed = self.changed_text.get("1.0", tk.END).splitlines()
        
        diff = difflib.unified_diff(original, changed, lineterm='')
        result = '\n'.join(list(diff))
        
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        
    def merge_changes(self):
        original = self.original_text.get("1.0", tk.END).splitlines()
        changed = self.changed_text.get("1.0", tk.END).splitlines()
        
        merged = list(difflib.ndiff(original, changed))
        merged_text = '\n'.join([line[2:] for line in merged if not line.startswith('- ')])
        
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, merged_text)
        
        messagebox.showinfo("Merge Complete", "The changes have been merged successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiffCheckerApp(root)
    root.mainloop()