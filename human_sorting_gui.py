import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re
from datetime import datetime

def sanitize_file_name(file_name):
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def get_latest_human_sorted_email_number():
    files = os.listdir("human_sorted")
    max_number = 0
    for file in files:
        if file.startswith("email_") and file.endswith(".txt"):
            number = int(file[6:-4].split("_")[0])
            if number > max_number:
                max_number = number
    return max_number

class EmailReviewApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Email Review")
        self.geometry("800x600")

        self.file_index = 0
        current_dir = os.getcwd()
        dir_name = "unsorted"
        directory_path = os.path.join(current_dir, dir_name)
        self.email_files = [f for f in os.listdir(os.path.join(os.getcwd(), "unsorted")) if f.startswith("email_") and f.endswith(".txt")]

        self.content = tk.Text(self, wrap=tk.WORD)
        self.content.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.rating_label = tk.Label(self, text="Rating (1-9):")
        self.rating_label.pack()
        self.rating_entry = tk.Entry(self)
        self.rating_entry.pack()

        self.classification_label = tk.Label(self, text="Classification:")
        self.classification_label.pack()
        self.classification_entry = tk.Entry(self)
        self.classification_entry.pack()

        self.save_button = tk.Button(self, text="Save", command=self.save_email)
        self.save_button.pack()

        self.next_button = tk.Button(self, text="Next", command=self.load_next_email)

        self.latest_human_sorted_email_number = get_latest_human_sorted_email_number()
        self.load_next_email()

    def load_next_email(self):
        if self.file_index >= len(self.email_files):
            messagebox.showinfo("Done", "All emails have been reviewed.")
            return

        file_name = self.email_files[self.file_index]
        print(file_name)
        with open("unsorted/" + file_name, "r", encoding="utf-8") as f:
            self.email_data = json.load(f)

        self.content.delete("1.0", tk.END)
        self.content.insert(tk.END, self.email_data["prompt"])
        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, self.email_data.get("rating", ""))
        self.classification_entry.delete(0, tk.END)
        self.classification_entry.insert(0, self.email_data.get("classification", ""))

    def save_email(self):
        rating = self.rating_entry.get().strip()
        classification = self.classification_entry.get().strip()

        if not rating or not classification:
            messagebox.showerror("Error", "Please enter both rating and classification.")
            return

        # Update the "completion" dictionary with the rating and classification
        completion = rating + ' ' + classification
        self.email_data["completion"] = completion

        # Only keep the "prompt" and "completion" data
        output_data = {
            "prompt": self.email_data["prompt"],
            "completion": self.email_data["completion"]
        }

        sender = self.email_data["email_sender"]
        subject = self.email_data["email_subject"]
        date = self.email_data["email_date"]
        date = date.replace(" ", "_")
        date = date[:-9]

        # Create a filename using the current human_sorted email number
        new_email_number = self.latest_human_sorted_email_number + 1
        new_file_name = f"email_{new_email_number}_{sender}_{date}.txt"
        new_file_name = new_file_name.replace(" ", "_")
        sanitized_file_name = sanitize_file_name(new_file_name)

        # Create the human_sorted folder if it doesn't exist
        cwd = os.getcwd()
        folder_name = 'human_sorted'
        folder_path = os.path.join(cwd, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Construct the file path inside the human_sorted folder
        file_path = os.path.join(folder_path, sanitized_file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        self.latest_human_sorted_email_number += 1
        self.file_index += 1
        self.load_next_email()

if __name__ == "__main__":
    app = EmailReviewApp()
    app.mainloop()
