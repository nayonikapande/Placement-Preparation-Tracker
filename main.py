import tkinter as tk
from tkinter import ttk, messagebox, filedialog
root = tk.Tk()
import customtkinter as ctk

#theme
bg_top="#FFF2B2"
bg_bottom="#A8C6E7"
sidebar_top="FFF2B2"
sidebar_bottom="#A8C6E7"
card_bg=ctk.CTkFrame(master=root, fg_color="transparent")
brown="674E45"
dark_amber="D97706"
amber="E19238"
light_amber="ECBB83"
peach="F8A29E"
muted="#92786B"
white="FFFFFF"

font_title=("Fraunces", 57.3)
font_heading=("Fraunces", 26.4)
font_body-("DM Sans", 10)
font_small=("DM Sans", 8.0)
font_big=("DM Sans", 12.0)

#sample data
JOBS = [
    ("Pinterest", "SDE Intern", "7.0", "₹12 LPA", "Open"),
    ("Amazon", "Graduate Engineer", "7.5", "₹18 LPA", "Open"),
    ("TCS", "Assistant System Engineer", "6.0", "₹3.6 LPA", "Open"),
    ("Microsoft", "Software Engineer", "8.0", "₹25 LPA", "Upcoming"),
]

APPLICATIONS = [
    ("Pinterest", "SDE Intern", "Applied", "26 Sep 2026"),
    ("Amazon", "Graduate Engineer", "Shortlisted", "27 Sep 2026"),
    ("TCS", "Assistant System Engineer", "Selected", "28 Sep 2026"),
    ("Microsoft", "Software Engineer", "Rejected", "29 Sep 2026"),
]

TESTS = [
    ("DSA", "18 Sep 2026", "78%"),
    ("Aptitude", "15 Sep 2026", "68%"),
    ("Python", "12 Sep 2026", "65%"),
]

INTERVIEWS = [
    ("Pinterest", "SDE Intern", "Technical Round", "Upcoming"),
    ("Amazon", "Graduate Engineer", "HR Round", "Upcoming"),
    ("TCS", "Assistant System Engineer", "Technical Round", "Completed"),
]

OFFERS = [
    ("TCS", "₹3.6 LPA", "28 Sep 2026", "Accepted"),
]

#Main Application
class PlacementTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Placement Preparation Tracker")
        self.geometry("1366x768")
        self.minsize(1050, 650)
        self.configure(bg=bg_bottom)

        self.role="Student"
        self.current_page="Login"

        self.sidebar=None
        self.topbar=None
        self.content=None

        self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def make_card(self, parent, title=None, bg=CARD_BG):
        card = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=brown,
            highlightthickness=1
        )

        if title:
            tk.Label(
                card,
                text=title,
                font=font_heading,
                bg=bg,
                fg=brown
            ).pack(anchor="w", padx=17, pady=(12, 7))

        return card

    def heading(self, parent, title, subtitle=""):
        tk.Label(parent, text=title, font=font_title, bg=bg_bottom, fg=brown).pack(anchor="w", pady=(12, 3))

        if subtitle:
            tk.Label(parent, text=subtitle, font=font_heading, bg=bg_bottom, fg=muted).pack(anchor="w", pady=(0, 18))

    def make_button(self, parent, text, command=None, bg="#ECBB83", fg=brown):
        return tk.Button(parent, text=text, command=command or self.placeholder_action, font=("Josefin Sans", 9, "bold"), bg=bg, fg=fg, activebackground="#ECBB83", activeforeground=brown, relief="flat", bd=0, padx=14, pady=9, cursor="hand2")

    def placeholder_action(self):
        messagebox.showinfo("Fontend prototype", "The UI is ready. This action will be connected to the backend later")

    def make_entry(self, parent, label, default=""):
        row = tk.Frame(parent, bg=parent.cget("bg"))
        row.pack(fill="x", padx=18, pady=6)

        tk.Label(
            row,
            text=label,
            width=21,
            anchor="w",
            font=font_big,
            fg=brown,
            bg=row.cget("bg")
        ).pack(side="left")

        entry = tk.Entry(
            row,
            font=font_big,
            relief="flat",
            bg=white,
            fg=brown
        )
        entry.insert(0, default)
        entry.pack(side="left", fill="x", expand=True, ipady=7)

        return entry

    def make_table(self, parent, headers, rows):
        table = tk.Frame(parent, bg=parent.cget("bg"))
        table.pack(fill="x", padx=15, pady=8)

        for col, header in enumerate(headers):
            tk.Label(
                table,
                text=header.upper(),
                font=font_small,
                fg=brown,
                bg="#E8DDAA",
                padx=8,
                pady=10
            ).grid(row=0, column=col, sticky="ew", padx=2, pady=2)

        for r, row_data in enumerate(rows, start=1):
            for c, value in enumerate(row_data):
                tk.Label(
                    table,
                    text=str(value),
                    font=font_big,
                    fg=BROWN,
                    bg=parent.cget("bg"),
                    padx=8,
                    pady=10,
                    anchor="w"
                ).grid(row=r, column=c, sticky="ew")

        for col in range(len(headers)):
            table.grid_columnconfigure(col, weight=1)

        return table

    def make_scrollable_area(self, parent):
        canvas = tk.Canvas(parent, bg=bg_bottom, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            parent, orient="vertical", command=canvas.yview
        )
        inner = tk.Frame(canvas, bg=bg_bottom)

        window_id = canvas.create_window(
            (0, 0), window=inner, anchor="nw"
        )

        inner.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                window_id, width=event.width
            )
        )

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return inner