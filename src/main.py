import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import random
import os
from pathlib import Path

class WatchlistRandomizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Watchlist Randomizer")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)
        
        # Load data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
    
    def load_data(self):
        try:
            # Get the path to the CSV file
            csv_path = Path("data/input/watchlist.csv")
            
            # Read the CSV file
            self.df = pd.read_csv(csv_path)
            
            # Extract unique values for dropdowns
            self.media_types = sorted(self.df["Type of Media"].unique())
            self.mediums = sorted(self.df["Medium"].unique())
            self.watched_options = sorted(self.df["Watched?"].unique())
            
            # Extract all tags
            all_tags = []
            for tags_str in self.df["Tags"].dropna():
                tags = [tag.strip() for tag in tags_str.split(",")]
                all_tags.extend(tags)
            self.tags = sorted(set(all_tags))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load watchlist data: {str(e)}")
            self.root.destroy()
    
    def create_widgets(self):
        # Create frame for filters
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # Type of Media dropdown
        ttk.Label(filter_frame, text="Type of Media:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.media_type_var = tk.StringVar(value="Any")
        media_type_dropdown = ttk.Combobox(filter_frame, textvariable=self.media_type_var, state="readonly")
        media_type_dropdown["values"] = ["Any"] + self.media_types
        media_type_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Medium dropdown
        ttk.Label(filter_frame, text="Medium:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.medium_var = tk.StringVar(value="Any")
        medium_dropdown = ttk.Combobox(filter_frame, textvariable=self.medium_var, state="readonly")
        medium_dropdown["values"] = ["Any"] + self.mediums
        medium_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Watched dropdown
        ttk.Label(filter_frame, text="Watched?:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.watched_var = tk.StringVar(value="Any")
        watched_dropdown = ttk.Combobox(filter_frame, textvariable=self.watched_var, state="readonly")
        watched_dropdown["values"] = ["Any"] + [str(option) for option in self.watched_options]
        watched_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Tags multiselect
        ttk.Label(filter_frame, text="Tags:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Create a frame for the tags listbox and scrollbar
        tags_frame = ttk.Frame(filter_frame)
        tags_frame.grid(row=0, column=3, rowspan=3, padx=5, pady=5, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tags_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox for tags
        self.tags_listbox = tk.Listbox(tags_frame, selectmode=tk.MULTIPLE, height=5, width=30)
        self.tags_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar
        self.tags_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tags_listbox.yview)
        
        # Populate the tags listbox
        for tag in self.tags:
            self.tags_listbox.insert(tk.END, tag)
        
        # Generate button
        generate_button = ttk.Button(self.root, text="Generate Random Selection", command=self.generate_random)
        generate_button.pack(pady=20)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.root, text="Result")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Result display
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10, width=60)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)
    
    def get_selected_tags(self):
        selected_indices = self.tags_listbox.curselection()
        return [self.tags_listbox.get(i) for i in selected_indices]
    
    def generate_random(self):
        # Get filter values
        media_type = self.media_type_var.get()
        medium = self.medium_var.get()
        watched = self.watched_var.get()
        selected_tags = self.get_selected_tags()
        
        # Filter the dataframe
        filtered_df = self.df.copy()
        
        if media_type != "Any":
            filtered_df = filtered_df[filtered_df["Type of Media"] == media_type]
        
        if medium != "Any":
            filtered_df = filtered_df[filtered_df["Medium"] == medium]
        
        if watched != "Any":
            # Convert string "TRUE"/"FALSE" to boolean if needed
            if watched.upper() == "TRUE":
                watched_value = True
            elif watched.upper() == "FALSE":
                watched_value = False
            else:
                watched_value = watched
            
            filtered_df = filtered_df[filtered_df["Watched?"].astype(str) == str(watched_value)]
        
        # Filter by tags if any are selected
        if selected_tags:
            # Keep only rows where at least one selected tag is in the Tags column
            tag_mask = filtered_df["Tags"].apply(
                lambda x: any(tag in str(x) for tag in selected_tags)
            )
            filtered_df = filtered_df[tag_mask]
        
        # Check if there are any matches
        if filtered_df.empty:
            messagebox.showinfo("No Matches", "No items match your filter criteria.")
            return
        
        # Select a random item
        random_item = filtered_df.sample(1).iloc[0]
        
        # Display the result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        result = f"Name: {random_item['Name']}\n"
        result += f"Type of Media: {random_item['Type of Media']}\n"
        result += f"Total Time Commitment: {random_item['Total Time Commitment']} hours\n"
        result += f"Medium: {random_item['Medium']}\n"
        result += f"Watched?: {random_item['Watched?']}\n"
        result += f"Tags: {random_item['Tags']}"
        
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatchlistRandomizer(root)
    root.mainloop()
