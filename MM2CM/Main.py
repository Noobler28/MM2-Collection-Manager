import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import time

from lists import weapons, CHROMA_COLOURS, RARITY_COLOURS

print("Loading, MM2 Collection Manager V3..")
print("Please Wait, Loading Resources...")
time.sleep(2)

WDATA_FILE = "weapons_data.json"
TDATA_FILE = "trading_data.json"
VDATA_FILE = "weapon_values.json"

def load_data():
    global weapons, trading_data
    print("Attempting to load data from", WDATA_FILE, "and", TDATA_FILE)
    
    # Load weapons data
    try:
        with open(WDATA_FILE, "r") as file:
            data = json.load(file)
        if isinstance(data, dict):
            weapons = data
            print("Weapons data loaded successfully.")
        else:
            print("Weapons data format incorrect. Using default data.")
            save_data()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading weapons data:", e)
        print("Saving default data.")
        save_data()

    # Load trading data
    try:
        with open(TDATA_FILE, "r") as file:
            trading_data = json.load(file)
        if not isinstance(trading_data, list):
            print("Trading data format incorrect. Using default empty list.")
            trading_data = []
            save_data()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading trading data:", e)
        trading_data = []
        save_data()

def save_data():
    try:
        with open(WDATA_FILE, "w") as file:
            json.dump(weapons, file, indent=4)
        
        with open(TDATA_FILE, "w") as file:
            json.dump(trading_data, file, indent=4)
    except Exception as e:
        print("Error saving data:", e)

class MM2CollectionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("MM2 Collection Manager V3 - By Connor")
        self.root.geometry("1050x470")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.tree = None 
        self.chroma = True
        self.search_results = []
        self.current_result_index = -1

        self.create_widgets()
        self.setup_trading_tracker_tab()
        self.setup_collection_manager_tab()
        self.setup_settings_tab()

        # Start Chroma animation after tree is created
        self.root.after(1000, self.animate_chroma)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Collection Manager")

        self.trading_tracker_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trading_tracker_tab, text="Trading Tracker")

        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")

    def setup_collection_manager_tab(self):
        control_frame = ttk.Frame(self.main_tab)
        control_frame.pack(fill="x", padx=10, pady=5)

        # Dropdown for categories
        ttk.Label(control_frame, text="Select Category:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(control_frame, textvariable=self.category_var)
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.category_dropdown['values'] = list(weapons.keys())
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_subcategories)

        # Dropdown for subcategories
        ttk.Label(control_frame, text="Select Subcategory:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.subcategory_var = tk.StringVar()
        self.subcategory_dropdown = ttk.Combobox(control_frame, textvariable=self.subcategory_var)
        self.subcategory_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.subcategory_dropdown.bind("<<ComboboxSelected>>", self.update_treeview)

        # Search bar
        ttk.Label(control_frame, text="Search:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        self.search_entry.bind("<Return>", self.search_weapons)

        # Treeview for weapons
        self.tree = ttk.Treeview(self.main_tab, columns=("Weapon", "Status", "Count", "Rarity", "Value"), show="headings")
        self.tree.heading("Weapon", text="Weapon")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Count", text="Count")
        self.tree.heading("Rarity", text="Rarity")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        for rarity, colour in RARITY_COLOURS.items():
            self.tree.tag_configure(rarity, foreground=colour)

        self.clear_treeview()

        # Update status button
        update_frame = ttk.Frame(self.main_tab)
        update_frame.pack(fill="x", padx=10, pady=5)

        self.update_status_button = ttk.Button(update_frame, text="Update Status", command=self.update_status)
        self.update_status_button.place(relx=0.5, rely=1.0, anchor="s")

        # Update count input and button
        ttk.Label(update_frame, text="Enter Count:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.count_var = tk.StringVar()
        self.count_entry = ttk.Entry(update_frame, textvariable=self.count_var, width=5)
        self.count_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.update_count_button = ttk.Button(update_frame, text="Update Count", command=self.update_count)
        self.update_count_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Next and Previous buttons
        self.prev_button = ttk.Button(self.main_tab, text="Previous", command=self.previous_result)
        self.prev_button.pack(side="left", padx=10, pady=5)
        self.next_button = ttk.Button(self.main_tab, text="Next", command=self.next_result)
        self.next_button.pack(side="right", padx=10, pady=5)

    def clear_treeview(self):
        self.tree.delete(*self.tree.get_children())

    def update_subcategories(self, event):
        category = self.category_var.get()
        if category in weapons:
            self.subcategory_dropdown['values'] = list(weapons[category].keys())
            self.update_treeview()

    def update_treeview(self, event=None):
        self.tree.delete(*self.tree.get_children())
        category = self.category_var.get()
        subcategory = self.subcategory_var.get()
        if category in weapons and subcategory in weapons[category]:
            for weapon, data in weapons[category][subcategory].items():
                rarity = data["Rarity"]
                tags = (rarity,)
                if rarity.lower() == "chroma":
                    tags = ("Chroma",)
                self.tree.insert("", "end", iid=weapon, values=(weapon, data["Status"], data["Count"], rarity, "NA"), tags=tags)

    def search_weapons(self, event=None):
        search_term = self.search_var.get().lower()
        self.search_results = []
        for category in weapons:
            for subcategory in weapons[category]:
                for weapon, data in weapons[category][subcategory].items():
                    if search_term in weapon.lower():
                        self.search_results.append((category, subcategory, weapon))
        self.current_result_index = -1
        self.next_result()

    def previous_result(self):
        if self.search_results:
            self.current_result_index = (self.current_result_index - 1) % len(self.search_results)
            self.select_search_result()

    def next_result(self):
        if self.search_results:
            self.current_result_index = (self.current_result_index + 1) % len(self.search_results)
            self.select_search_result()

    def select_search_result(self):
        if self.search_results:
            category, subcategory, weapon = self.search_results[self.current_result_index]
            self.category_var.set(category)
            self.update_subcategories(None)
            self.subcategory_var.set(subcategory)
            self.update_treeview()
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[0] == weapon:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    break

    def update_status(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            weapon_name = self.tree.item(selected_item, "values")[0]
            for category in weapons:
                for subcategory in weapons[category]:
                    if weapon_name in weapons[category][subcategory]:
                        current_status = weapons[category][subcategory][weapon_name]["Status"]
                        new_status = "Collected" if current_status != "Collected" else "Not Collected"
                        self.tree.set(selected_item, "Status", new_status)
                        weapons[category][subcategory][weapon_name]["Status"] = new_status
                        save_data()
                        break

    def update_count(self):
        selected_item = self.tree.selection()
        if selected_item:
            try:
                new_count = int(self.count_var.get())
                if new_count >= 0:
                    self.tree.set(selected_item, "Count", new_count)
                    weapon_name = self.tree.item(selected_item, "values")[0]
                    for category in weapons:
                        for subcategory in weapons[category]:
                            if weapon_name in weapons[category][subcategory]:
                                weapons[category][subcategory][weapon_name]["Count"] = new_count
                                save_data()
                                break
                else:
                    messagebox.showerror("Invalid Count", "Count must be 0 or greater.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the count.")

    def populate_tree(self):
        for category in weapons:
            for subcategory in weapons[category]:
                for weapon, data in weapons[category][subcategory].items():
                    rarity = data["Rarity"]
                    tags = (rarity,)
                    if rarity.lower() == "chroma":
                        tags = ("Chroma",)
                    self.tree.insert("", "end", iid=weapon, values=(weapon, data["Status"], data["Count"], rarity, "NA"), tags=tags)

    # Trading Tracker Tab
    def setup_trading_tracker_tab(self):
        frame = ttk.Frame(self.trading_tracker_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(frame, text="Items Gave:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.added_entry = ttk.Entry(frame, width=30)
        self.added_entry.grid(row=0, column=1, padx=5, pady=2)
        self.added_entry.bind("<KeyRelease>", self.update_added_recommendations)

        self.added_recommendations = tk.Listbox(frame, width=30)
        self.added_recommendations.grid(row=1, column=1, padx=5, pady=2)
        self.added_recommendations.bind("<<ListboxSelect>>", self.select_added_recommendation)
        self.added_recommendations.grid_remove()

        ttk.Label(frame, text="Items Received:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.received_entry = ttk.Entry(frame, width=30)
        self.received_entry.grid(row=2, column=1, padx=5, pady=2)
        self.received_entry.bind("<KeyRelease>", self.update_received_recommendations)

        self.received_recommendations = tk.Listbox(frame, width=30)
        self.received_recommendations.grid(row=3, column=1, padx=5, pady=2)
        self.received_recommendations.bind("<<ListboxSelect>>", self.select_received_recommendation)
        self.received_recommendations.grid_remove()

        self.add_trade_button = ttk.Button(frame, text="Add Trade", command=self.add_trade)
        self.add_trade_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.trade_table = ttk.Treeview(frame, columns=("Added", "Received"), show="headings")
        self.trade_table.heading("Added", text="You Added")
        self.trade_table.heading("Received", text="They Added")
        self.trade_table.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=5)
        self.trade_table.bind("<Double-1>", self.show_trade_details)

        for rarity, colour in RARITY_COLOURS.items():
            self.trade_table.tag_configure(rarity, foreground=colour)

        self.trade_details_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trade_details_tab, text="Trade Details")
        self.notebook.hide(self.trade_details_tab)

    def update_added_recommendations(self, event):
        search_term = self.added_entry.get().lower()
        self.added_recommendations.delete(0, tk.END)
        if search_term:
            for category in weapons:
                for subcategory in weapons[category]:
                    for weapon in weapons[category][subcategory]:
                        if search_term in weapon.lower():
                            self.added_recommendations.insert(tk.END, weapon)
            self.added_recommendations.grid()
        else:
            self.added_recommendations.grid_remove()

    def select_added_recommendation(self, event):
        if self.added_recommendations.curselection():
            selected_item = self.added_recommendations.get(self.added_recommendations.curselection())
            self.added_entry.delete(0, tk.END)
            self.added_entry.insert(0, selected_item)
            self.added_recommendations.grid_remove()

    def update_received_recommendations(self, event):
        search_term = self.received_entry.get().lower()
        self.received_recommendations.delete(0, tk.END)
        if search_term:
            for category in weapons:
                for subcategory in weapons[category]:
                    for weapon in weapons[category][subcategory]:
                        if search_term in weapon.lower():
                            self.received_recommendations.insert(tk.END, weapon)
            self.received_recommendations.grid()
        else:
            self.received_recommendations.grid_remove()

    def select_received_recommendation(self, event):
        if self.received_recommendations.curselection():
            selected_item = self.received_recommendations.get(self.received_recommendations.curselection())
            self.received_entry.delete(0, tk.END)
            self.received_entry.insert(0, selected_item)
            self.received_recommendations.grid_remove()

    def add_trade(self):
        added_items = self.added_entry.get().split(",")
        received_items = self.received_entry.get().split(",")
        if added_items and received_items:
            added_tags = [self.get_rarity_tag(item.strip()) for item in added_items]
            received_tags = [self.get_rarity_tag(item.strip()) for item in received_items]
            self.trade_table.insert("", "end", values=(self.format_items(added_items), self.format_items(received_items)), tags=added_tags + received_tags)
            trading_data.append({"Added": self.format_items(added_items), "Received": self.format_items(received_items)})
            save_data()
            self.added_entry.delete(0, tk.END)
            self.received_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Trade", "Both fields must be filled out.")

    def get_rarity_tag(self, item):
        for category in weapons:
            for subcategory in weapons[category]:
                if item in weapons[category][subcategory]:
                    return weapons[category][subcategory][item]["Rarity"]
        return ""

    def format_items(self, items):
        return ", ".join(items)

    def show_trade_details(self, event):
        selected_item = self.trade_table.selection()
        if selected_item:
            selected_item = selected_item[0]
            trade = self.trade_table.item(selected_item, "values")
            self.notebook.tab(self.trade_details_tab, text="Trade Details")
            self.notebook.select(self.trade_details_tab)
            for widget in self.trade_details_tab.winfo_children():
                widget.destroy()

            details_frame = ttk.Frame(self.trade_details_tab, padding="10")
            details_frame.pack(fill="both", expand=True)

            ttk.Label(details_frame, text="Trader's Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=5)
            self.trader_name_entry = ttk.Entry(details_frame, width=30)
            self.trader_name_entry.grid(row=0, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Items You Added:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=trade[0], font=("Arial", 10)).grid(row=1, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Items You Received:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=trade[1], font=("Arial", 10)).grid(row=2, column=1, sticky="w", pady=5)

            added_value = self.calculate_value(trade[0])
            received_value = self.calculate_value(trade[1])
            value_difference = received_value - added_value

            ttk.Label(details_frame, text="Value of Items You Added:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=str(added_value), font=("Arial", 10)).grid(row=3, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Value of Items You Received:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=str(received_value), font=("Arial", 10)).grid(row=4, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Value Difference:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=str(value_difference), font=("Arial", 10)).grid(row=5, column=1, sticky="w", pady=5)

            ttk.Button(details_frame, text="Back", command=self.hide_trade_details).grid(row=6, column=0, pady=10)
            ttk.Button(details_frame, text="Remove Trade", command=lambda: self.remove_trade(selected_item)).grid(row=6, column=1, pady=10)

    def remove_trade(self, item_id):
        trade_values = self.trade_table.item(item_id, "values")
        self.trade_table.delete(item_id)
        for trade in trading_data:
            if trade["Added"] == trade_values[0] and trade["Received"] == trade_values[1]:
                trading_data.remove(trade)
                save_data()
                break
        self.hide_trade_details()

    def calculate_value(self, items):
        # Placeholder function to calculate the value of items
        # FOR SELF: Replace with actual logic to calculate item values (when values are implemented)
        return sum([int(item.split()[-1]) for item in items.split(",") if item.split()[-1].isdigit()])

    def hide_trade_details(self):
        self.notebook.hide(self.trade_details_tab)
        self.notebook.select(self.trading_tracker_tab)

    # Settings Tab
    def setup_settings_tab(self):
        ttk.Label(self.settings_tab, text="Placeholder", font=("Arial", 14)).pack(pady=20)

    def animate_chroma(self, index=0):
        """Animate Chroma text color cycling through CHROMA_COLOURS."""
        if self.chroma and self.tree is not None:
            colour = CHROMA_COLOURS[index]
            self.tree.tag_configure("Chroma", foreground=colour)
            self.root.after(500, self.animate_chroma, (index + 1) % len(CHROMA_COLOURS))

load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = MM2CollectionManager(root)
    root.mainloop()
