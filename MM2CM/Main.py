import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import time
from PIL import Image, ImageTk  # Add this import for handling images

from lists import weapons, CHROMA_COLOURS, RARITY_COLOURS, EVO_COLOURS

print("Loading, MM2 Collection Manager V3..")
print("Please Wait, Loading Resources...")
time.sleep(2)

WDATA_FILE = "weapons_data.json"
TDATA_FILE = "trading_data.json"
VDATA_FILE = "weapon_values.json"
SDATA_FILE = "settings_data.json"

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

        self.dark_mode = tk.BooleanVar(value=False)
        self.chroma_animation = tk.BooleanVar(value=True)
        self.evo_animation = tk.BooleanVar(value=True)

        self.tree = None 
        self.chroma = True
        self.search_results = []
        self.current_result_index = -1

        self.create_widgets()
        self.setup_trading_tracker_tab()
        self.setup_collection_manager_tab()
        self.setup_settings_tab()
        self.load_trading_data()

        # Start Chroma animation after tree is created
        self.root.after(1000, self.animate_chroma)
        self.root.after(1000, self.animate_evo)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Collection Manager")

        self.weapon_details_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.weapon_details_tab, text="Weapon Details")
        self.notebook.hide(self.weapon_details_tab)

        self.trading_tracker_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trading_tracker_tab, text="Trading Tracker")

        # Trade Offers tab
        self.trade_offers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trade_offers_tab, text="Trade Offers")
        
        # Placeholder content for Trade Offers tab
        ttk.Label(self.trade_offers_tab, text="Trade Offers Placeholder", font=("Arial", 14)).pack(pady=20)

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

        # Search bar with dropdown for filters
        search_frame = ttk.Frame(control_frame)
        search_frame.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.update_search_recommendations)
        self.search_entry.bind("<Return>", self.search_weapons)

        self.filter_button = ttk.Button(search_frame, text="Search Filters", command=self.toggle_filters)
        self.filter_button.pack(side="right")

        self.filter_frame = ttk.Frame(control_frame)
        self.filter_frame.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.filter_frame.grid_remove()

        # Filters
        ttk.Label(self.filter_frame, text="Rarity:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.rarity_vars = {rarity: tk.BooleanVar() for rarity in RARITY_COLOURS.keys()}
        for i, (rarity, color) in enumerate(RARITY_COLOURS.items()):
            checkbutton = ttk.Checkbutton(self.filter_frame, text=rarity, variable=self.rarity_vars[rarity])
            checkbutton.grid(row=i+1, column=0, sticky="w")
            checkbutton.configure(style=f"{rarity}.TCheckbutton")
            self.style.configure(f"{rarity}.TCheckbutton", foreground=color)

        ttk.Label(self.filter_frame, text="Type:").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.type_vars = {"Gun": tk.BooleanVar(), "Knife": tk.BooleanVar()}
        for i, weapon_type in enumerate(self.type_vars.keys()):
            ttk.Checkbutton(self.filter_frame, text=weapon_type, variable=self.type_vars[weapon_type]).grid(row=i+1, column=1, sticky="w")

        ttk.Label(self.filter_frame, text="Status:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.status_vars = {"Collected": tk.BooleanVar(), "Not Collected": tk.BooleanVar()}
        for i, status in enumerate(self.status_vars.keys()):
            ttk.Checkbutton(self.filter_frame, text=status, variable=self.status_vars[status]).grid(row=i+1, column=2, sticky="w")

        # Search recommendations listbox
        self.search_recommendations = tk.Listbox(control_frame, width=30)
        self.search_recommendations.grid(row=1, column=4, padx=5, pady=2, sticky="w")
        self.search_recommendations.bind("<<ListboxSelect>>", self.select_search_recommendation)
        self.search_recommendations.grid_remove()

        # Treeview for weapons
        self.tree = ttk.Treeview(self.main_tab, columns=("Weapon", "Status", "Count", "Rarity", "Value"), show="headings")
        self.tree.heading("Weapon", text="Weapon")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Count", text="Count")
        self.tree.heading("Rarity", text="Rarity")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<Double-1>", self.show_weapon_details)

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

    def toggle_filters(self):
        if self.filter_frame.winfo_ismapped():
            self.filter_frame.grid_remove()
        else:
            self.filter_frame.grid()

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
            items = []
            for sub_subcategory in weapons[category][subcategory]:
                for weapon, data in weapons[category][subcategory][sub_subcategory].items():
                    items.append((weapon, data))
            
            # Sort items by rarity
            items.sort(key=lambda x: list(RARITY_COLOURS.keys()).index(x[1]["Rarity"]))

            for index, (weapon, data) in enumerate(items):
                rarity = data["Rarity"]
                tags = (rarity,)
                if rarity.lower() == "chroma":
                    tags = ("Chroma",)
                self.tree.insert("", "end", iid=f"{weapon}_{index}", values=(weapon, data["Status"], data["Count"], rarity, "NA"), tags=tags)

    def update_search_recommendations(self, event):
        search_term = self.search_var.get().lower()
        self.search_recommendations.delete(0, tk.END)
        if search_term:
            for category in weapons:
                for subcategory in weapons[category]:
                    for sub_subcategory in weapons[category][subcategory]:
                        for weapon in weapons[category][subcategory][sub_subcategory]:
                            if search_term in weapon.lower():
                                self.search_recommendations.insert(tk.END, weapon)
            self.search_recommendations.grid()
        else:
            self.search_recommendations.grid_remove()

    def select_search_recommendation(self, event):
        if self.search_recommendations.curselection():
            selected_item = self.search_recommendations.get(self.search_recommendations.curselection())
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, selected_item)
            self.search_recommendations.grid_remove()
            self.search_weapons()

    def search_weapons(self, event=None):
        self.search_recommendations.grid_remove()
        search_term = self.search_var.get().lower()
        selected_rarities = [rarity for rarity, var in self.rarity_vars.items() if var.get()]
        selected_types = [weapon_type.lower() for weapon_type, var in self.type_vars.items() if var.get()]
        selected_statuses = [status for status, var in self.status_vars.items() if var.get()]

        self.search_results = []
        for category in weapons:
            for subcategory in weapons[category]:
                for sub_subcategory in weapons[category][subcategory]:
                    for weapon, data in weapons[category][subcategory][sub_subcategory].items():
                        if search_term in weapon.lower():
                            if selected_rarities and data["Rarity"] not in selected_rarities:
                                continue
                            if selected_types and sub_subcategory.lower() not in selected_types:
                                continue
                            if selected_statuses and data["Status"] not in selected_statuses:
                                continue
                            self.search_results.append((category, subcategory, sub_subcategory, weapon))
        self.current_result_index = -1
        self.next_result()
        self.search_entry.delete(0, tk.END)

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
            category, subcategory, sub_subcategory, weapon = self.search_results[self.current_result_index]
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
                    for sub_subcategory in weapons[category][subcategory]:
                        if weapon_name in weapons[category][subcategory][sub_subcategory]:
                            current_status = weapons[category][subcategory][sub_subcategory][weapon_name]["Status"]
                            new_status = "Collected" if current_status != "Collected" else "Not Collected"
                            self.tree.set(selected_item, "Status", new_status)
                            weapons[category][subcategory][sub_subcategory][weapon_name]["Status"] = new_status
                            save_data()
                            break

    def update_count(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]

            try:
                new_count = int(self.count_var.get())
                if new_count < 0:
                    messagebox.showerror("Invalid Count", "Count must be 0 or greater.")
                    return

                item_values = self.tree.item(selected_item, "values")
                if not item_values:
                    messagebox.showerror("Selection Error", "Could not retrieve item values.")
                    return

                weapon_name = item_values[0]

                for category in weapons:
                    for subcategory in weapons[category]:
                        for sub_subcategory in weapons[category][subcategory]:
                            if weapon_name in weapons[category][subcategory][sub_subcategory]:
                                weapons[category][subcategory][sub_subcategory][weapon_name]["Count"] = new_count
                                self.tree.set(selected_item, "Count", new_count)
                                save_data()
                                return

                messagebox.showerror("Weapon Not Found", f"Could not find {weapon_name} in weapon data.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the count.")


    def populate_tree(self):
        for category in weapons:
            for subcategory in weapons[category]:
                for sub_subcategory in weapons[category][subcategory]:
                    for weapon, data in weapons[category][subcategory][sub_subcategory].items():
                        rarity = data["Rarity"]
                        tags = (rarity,)
                        if rarity.lower() == "chroma":
                            tags = ("Chroma",)
                        self.tree.insert("", "end", iid=weapon, values=(weapon, data["Status"], data["Count"], rarity, "NA"), tags=tags)

    def show_weapon_details(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            weapon = self.tree.item(selected_item, "values")
            self.notebook.tab(self.weapon_details_tab, text="Weapon Details")
            self.notebook.select(self.weapon_details_tab)
            for widget in self.weapon_details_tab.winfo_children():
                widget.destroy()

            details_frame = ttk.Frame(self.weapon_details_tab, padding="10")
            details_frame.pack(fill="both", expand=True)

            # Load and display weapon image
            weapon_name = weapon[0].replace(" ", "")
            subcategory = self.subcategory_var.get().replace(" ", "")
            rarity = weapon[3].replace(" ", "")
            image_path = f"weapon_images/{subcategory}/{weapon_name}_{subcategory}_{rarity}.png"
            try:
                image = Image.open(image_path)
                image = image.resize((300, 200), Image.LANCZOS)
                weapon_image = ImageTk.PhotoImage(image)
                self.weapon_image_canvas = tk.Canvas(details_frame, width=300, height=200)
                self.weapon_image_canvas.create_image(150, 100, image=weapon_image)
                self.weapon_image_canvas.image = weapon_image  # Keep a reference to avoid garbage collection
            except FileNotFoundError:
                self.weapon_image_canvas = tk.Canvas(details_frame, width=300, height=200, background="gray")
                self.weapon_image_canvas.create_text(150, 100, text="Image Not Found", font=("Arial", 12, "bold"))
            self.weapon_image_canvas.grid(row=0, column=0, columnspan=2, pady=10)

            ttk.Label(details_frame, text="Weapon Name:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=weapon[0], font=("Arial", 10)).grid(row=1, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Status:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=weapon[1], font=("Arial", 10)).grid(row=2, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Count:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=weapon[2], font=("Arial", 10)).grid(row=3, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Rarity:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=weapon[3], font=("Arial", 10)).grid(row=4, column=1, sticky="w", pady=5)

            ttk.Label(details_frame, text="Value:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w", pady=5)
            ttk.Label(details_frame, text=weapon[4], font=("Arial", 10)).grid(row=5, column=1, sticky="w", pady=5)

            ttk.Button(details_frame, text="Back", command=lambda: self.hide_weapon_details()).grid(row=6, column=0, columnspan=2, pady=10)

    def hide_weapon_details(self):
        self.notebook.hide(self.weapon_details_tab)
        self.notebook.select(self.main_tab)

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

        self.trade_details_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trade_details_tab, text="Trade Details")
        self.notebook.hide(self.trade_details_tab)

        # Info button
        self.info_button = ttk.Button(frame, text="Info", command=self.show_info)
        self.info_button.grid(row=6, column=0, columnspan=2, pady=5)

    def show_info(self):
        info_message = (
            "How to use the Trading Tracker:\n\n"
            "1. Adding Trades:\n"
            "   - Enter the items you gave in the 'Items Gave' field.\n"
            "   - Enter the items you received in the 'Items Received' field.\n"
            "   - Click 'Add Trade' to save the trade.\n\n"
            "2. Removing Trades:\n"
            "   - Double-click on a trade in the table to view details.\n"
            "   - Click 'Remove Trade' to delete the trade.\n\n"
            "3. Adding Trader's Name:\n"
            "   - Double-click on a trade in the table to view details.\n"
            "   - Enter the trader's name in the 'Trader's Name' field.\n"
            "   - Click 'Back' to return to the main trading tracker.\n\n"
            "4. Viewing Trade Details:\n"
            "   - Double-click on a trade in the table to view details.\n"
            "   - View the items you added, received, and the value difference.\n"
            "   - The value difference is based on an ESTIMATED value, and may not be accurate\n\n"
        )
        messagebox.showinfo("Trading Tracker Info", info_message)

    def load_trading_data(self):
        """Load trading data into the trade table."""
        for trade in trading_data:
            self.trade_table.insert("", "end", values=(trade["Added"], trade["Received"]))

    def update_added_recommendations(self, event):
        search_term = self.added_entry.get().lower().split(",")[-1].strip()
        self.added_recommendations.delete(0, tk.END)
        if search_term:
            for category in weapons:
                for subcategory in weapons[category]:
                    for sub_subcategory in weapons[category][subcategory]:
                        for weapon in weapons[category][subcategory][sub_subcategory]:
                            if search_term in weapon.lower():
                                self.added_recommendations.insert(tk.END, weapon)
            self.added_recommendations.grid()
        else:
            self.added_recommendations.grid_remove()
        self.root.after(1, self.added_entry.focus_set)  # Ensure the input box remains selected

    def select_added_recommendation(self, event):
        if self.added_recommendations.curselection():
            selected_item = self.added_recommendations.get(self.added_recommendations.curselection())
            current_text = self.added_entry.get()
            if "," in current_text:
                self.added_entry.delete(0, tk.END)
                self.added_entry.insert(0, f"{current_text.rsplit(',', 1)[0]}, {selected_item}")
            else:
                self.added_entry.delete(0, tk.END)
                self.added_entry.insert(0, selected_item)
            self.added_recommendations.grid_remove()
            self.root.after(1, self.added_entry.focus_set)  # Ensure the input box remains selected

    def update_received_recommendations(self, event):
        search_term = self.received_entry.get().lower().split(",")[-1].strip()
        self.received_recommendations.delete(0, tk.END)
        if search_term:
            for category in weapons:
                for subcategory in weapons[category]:
                    for sub_subcategory in weapons[category][subcategory]:
                        for weapon in weapons[category][subcategory][sub_subcategory]:
                            if search_term in weapon.lower():
                                self.received_recommendations.insert(tk.END, weapon)
            self.received_recommendations.grid()
        else:
            self.received_recommendations.grid_remove()
        self.root.after(1, self.received_entry.focus_set)  # Ensure the input box remains selected

    def select_received_recommendation(self, event):
        if self.received_recommendations.curselection():
            selected_item = self.received_recommendations.get(self.received_recommendations.curselection())
            current_text = self.received_entry.get()
            if "," in current_text:
                self.received_entry.delete(0, tk.END)
                self.received_entry.insert(0, f"{current_text.rsplit(',', 1)[0]}, {selected_item}")
            else:
                self.received_entry.delete(0, tk.END)
                self.received_entry.insert(0, selected_item)
            self.received_recommendations.grid_remove()
            self.root.after(1, self.received_entry.focus_set)  # Ensure the input box remains selected

    def add_trade(self):
        added_items = self.added_entry.get().strip().split(",")
        received_items = self.received_entry.get().strip().split(",")
        
        # Ensure at least one side is not empty
        if not any(added_items) and not any(received_items):
            messagebox.showerror("Invalid Trade", "Both fields cannot be empty.")
            return
        
        added_items = [item.strip() for item in added_items if item.strip()]
        received_items = [item.strip() for item in received_items if item.strip()]
        
        self.trade_table.insert("", "end", values=(self.format_items(added_items), self.format_items(received_items)))
        trading_data.append({"Added": self.format_items(added_items), "Received": self.format_items(received_items)})
        save_data()
        self.added_entry.delete(0, tk.END)
        self.received_entry.delete(0, tk.END)

    def remove_trade(self, item_id):
        trade_values = self.trade_table.item(item_id, "values")
        self.trade_table.delete(item_id)
        for trade in trading_data:
            if trade["Added"] == trade_values[0] and trade["Received"] == trade_values[1]:
                trading_data.remove(trade)
                save_data()
                break
        self.hide_trade_details()

    def get_rarity_tag(self, item):
        for category in weapons:
            for subcategory in weapons[category]:
                for sub_subcategory in weapons[category][subcategory]:
                    if item in weapons[category][subcategory][sub_subcategory]:
                        return weapons[category][subcategory][sub_subcategory][item]["Rarity"]
        return ""

    def format_items(self, items):
        return ", ".join(items)

    def calculate_value(self, items):
        """Calculate the value of items. Placeholder logic."""
        total_value = 0
        for item in items.split(","):
            parts = item.split()
            if parts and parts[-1].isdigit():
                total_value += int(parts[-1])
        return total_value

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

            # Set the trader's name if it exists
            for trade_data in trading_data:
                if trade_data["Added"] == trade[0] and trade_data["Received"] == trade[1]:
                    self.trader_name_entry.insert(0, trade_data.get("Trader", ""))
                    break

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

            ttk.Button(details_frame, text="Save User", command=lambda: self.save_trader_name(selected_item)).grid(row=6, column=0, pady=10)
            ttk.Button(details_frame, text="Remove User", command=lambda: self.remove_trader_name(selected_item)).grid(row=6, column=1, pady=10)
            ttk.Button(details_frame, text="Back", command=lambda: self.hide_trade_details()).grid(row=7, column=0, pady=10)
            ttk.Button(details_frame, text="Remove Trade", command=lambda: self.remove_trade(selected_item)).grid(row=7, column=1, pady=10)

    def save_trader_name(self, item_id):
        trader_name = self.trader_name_entry.get()
        if trader_name:
            for trade in trading_data:
                if trade["Added"] == self.trade_table.item(item_id, "values")[0] and trade["Received"] == self.trade_table.item(item_id, "values")[1]:
                    trade["Trader"] = trader_name
                    save_data()
                    break

    def remove_trader_name(self, item_id):
        for trade in trading_data:
            if trade["Added"] == self.trade_table.item(item_id, "values")[0] and trade["Received"] == self.trade_table.item(item_id, "values")[1]:
                if "Trader" in trade:
                    del trade["Trader"]
                    save_data()
                    break

    def hide_trade_details(self):
        self.notebook.hide(self.trade_details_tab)
        self.notebook.select(self.trading_tracker_tab)

    # Settings Tab
    def setup_settings_tab(self):
        settings_notebook = ttk.Notebook(self.settings_tab)
        settings_notebook.pack(fill="both", expand=True)

        # General settings tab
        general_settings_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(general_settings_tab, text="General")

        ttk.Label(general_settings_tab, text="General Settings", font=("Arial", 14)).pack(pady=20)

        # Auto scan settings frame
        auto_scan_frame = ttk.Frame(general_settings_tab)
        auto_scan_frame.pack(pady=10)

        # Auto scan trade setting
        ttk.Label(auto_scan_frame, text="Auto Scan Trade:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.auto_scan_trade_var = tk.StringVar(value="Off")
        self.auto_scan_trade_switch = ttk.OptionMenu(auto_scan_frame, self.auto_scan_trade_var, "Off", "Off", "Live scan", "Screenshots")
        self.auto_scan_trade_switch.grid(row=0, column=1, padx=10, pady=5)

        # Auto scan inventory setting
        ttk.Label(auto_scan_frame, text="Auto Scan Inventory:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
        self.auto_scan_inventory_var = tk.StringVar(value="Off")
        self.auto_scan_inventory_switch = ttk.OptionMenu(auto_scan_frame, self.auto_scan_inventory_var, "Off", "Off", "Live scan", "Screenshots")
        self.auto_scan_inventory_switch.grid(row=0, column=3, padx=10, pady=5)

        # Appearance settings tab
        appearance_settings_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(appearance_settings_tab, text="Appearance")

        ttk.Label(appearance_settings_tab, text="Appearance Settings", font=("Arial", 14)).pack(pady=20)
        
        # Dark mode toggle
        self.dark_mode_checkbutton = ttk.Checkbutton(appearance_settings_tab, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode)
        self.dark_mode_checkbutton.pack(pady=10)

        # Chroma animation toggle
        self.chroma_animation_checkbutton = ttk.Checkbutton(appearance_settings_tab, text="Chroma Animation", variable=self.chroma_animation, command=self.toggle_chroma_animation)
        self.chroma_animation_checkbutton.pack(pady=10)

        # EVO animation toggle
        self.evo_animation_checkbutton = ttk.Checkbutton(appearance_settings_tab, text="EVO Animation", variable=self.evo_animation, command=self.toggle_evo_animation)
        self.evo_animation_checkbutton.pack(pady=10)

        # Font size setting
        ttk.Label(appearance_settings_tab, text="Font Size:", font=("Arial", 12)).pack(pady=10)
        self.font_size_var = tk.IntVar(value=10)
        self.font_size_spinbox = ttk.Spinbox(appearance_settings_tab, from_=8, to=20, textvariable=self.font_size_var, command=self.update_font_size)
        self.font_size_spinbox.pack(pady=5)

        # Advanced settings tab
        advanced_settings_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(advanced_settings_tab, text="Advanced")

        ttk.Label(advanced_settings_tab, text="Advanced Settings", font=("Arial", 14)).pack(pady=20)
        
        # Placeholder for advanced settings
        ttk.Label(advanced_settings_tab, text="Placeholder for advanced settings").pack(pady=10)

    def toggle_auto_scan_trade(self):
        if self.auto_scan_trade_var.get() == "Live scan":
            self.auto_scan_trade_switch.config(text="Live scan")
        else:
            self.auto_scan_trade_switch.config(text="Screenshots")

    def toggle_auto_scan_inventory(self):
        if self.auto_scan_inventory_var.get() == "Live scan":
            self.auto_scan_inventory_switch.config(text="Live scan")
        else:
            self.auto_scan_inventory_switch.config(text="Screenshots")

    def update_font_size(self):
        font_size = self.font_size_var.get()
        self.style.configure("TLabel", font=("Arial", font_size))
        self.style.configure("TButton", font=("Arial", font_size))
        self.style.configure("TCheckbutton", font=("Arial", font_size))
        self.style.configure("TEntry", font=("Arial", font_size))
        self.style.configure("TCombobox", font=("Arial", font_size))
        self.style.configure("Treeview", font=("Arial", font_size))
        self.style.configure("Treeview.Heading", font=("Arial", font_size))
        self.style.configure("TNotebook.Tab", font=("Arial", font_size))

    def toggle_dark_mode(self):
        if self.dark_mode.get():
            self.style.theme_use("alt")
            self.style.configure("TFrame", background="#2e2e2e")
            self.style.configure("TLabel", background="#2e2e2e", foreground="white")
            self.style.configure("TButton", background="#2e2e2e", foreground="white")
            self.style.configure("TCheckbutton", background="#2e2e2e", foreground="white")
            self.style.configure("TEntry", fieldbackground="#2e2e2e", foreground="white")
            self.style.configure("TCombobox", fieldbackground="#2e2e2e", foreground="white")
            self.style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
            self.style.configure("Treeview.Heading", background="#2e2e2e", foreground="white")
            self.style.configure("TNotebook", background="#2e2e2e")
            self.style.configure("TNotebook.Tab", background="#2e2e2e", foreground="white")
            self.root.configure(bg="#2e2e2e")
            self.root.option_add("*TNotebook*Tab*background", "#2e2e2e")
            self.root.option_add("*TNotebook*Tab*foreground", "white")
            self.root.option_add("*TCheckbutton*Indicator*background", "#2e2e2e")
            self.root.option_add("*TCheckbutton*Indicator*foreground", "white")
            self.style.map("TCheckbutton", background=[("selected", "#2e2e2e")], foreground=[("selected", "white")])
            self.update_filter_styles(dark_mode=True)
        else:
            self.style.theme_use("clam")
            self.style.configure("TFrame", background="SystemButtonFace")
            self.style.configure("TLabel", background="SystemButtonFace", foreground="black")
            self.style.configure("TButton", background="SystemButtonFace", foreground="black")
            self.style.configure("TCheckbutton", background="SystemButtonFace", foreground="black")
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("TCombobox", fieldbackground="white", foreground="black")
            self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
            self.style.configure("Treeview.Heading", background="SystemButtonFace", foreground="black")
            self.style.configure("TNotebook", background="SystemButtonFace")
            self.style.configure("TNotebook.Tab", background="SystemButtonFace", foreground="black")
            self.root.configure(bg="SystemButtonFace")
            self.root.option_add("*TNotebook*Tab*background", "SystemButtonFace")
            self.root.option_add("*TNotebook*Tab*foreground", "black")
            self.root.option_add("*TCheckbutton*Indicator*background", "SystemButtonFace")
            self.root.option_add("*TCheckbutton*Indicator*foreground", "black")
            self.style.map("TCheckbutton", background=[("selected", "SystemButtonFace")], foreground=[("selected", "black")])
            self.update_filter_styles(dark_mode=False)

    def update_filter_styles(self, dark_mode):
        for rarity, color in RARITY_COLOURS.items():
            if dark_mode:
                self.style.configure(f"{rarity}.TCheckbutton", foreground=color, background="#2e2e2e")
            else:
                self.style.configure(f"{rarity}.TCheckbutton", foreground=color, background="SystemButtonFace")

    def toggle_chroma_animation(self):
        if self.chroma_animation.get():
            self.chroma = True
            self.animate_chroma()
        else:
            self.chroma = False
            self.tree.tag_configure("Chroma", foreground=CHROMA_COLOURS[4])

    def animate_chroma(self, index=0):
        """Animate Chroma text color cycling through CHROMA_COLOURS."""
        if self.chroma and self.tree is not None:
            colour = CHROMA_COLOURS[index]
            self.tree.tag_configure("Chroma", foreground=colour)
            self.root.after(500, self.animate_chroma, (index + 1) % len(CHROMA_COLOURS))

    def animate_evo(self, index=0):
        """Animate EVO text color cycling through EVO_COLOURS."""
        if self.evo_animation.get() and self.tree is not None:
            colour = EVO_COLOURS[index]
            self.tree.tag_configure("EVO", foreground=colour)
            self.root.after(500, self.animate_evo, (index + 1) % len(EVO_COLOURS))

    def toggle_evo_animation(self):
        if self.evo_animation.get():
            self.animate_evo()
        else:
            self.tree.tag_configure("EVO", foreground=EVO_COLOURS[0])

load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = MM2CollectionManager(root)
    root.mainloop()
