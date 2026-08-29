import calendar
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import json

"""
Dark mode1:
    BG#0E131F
    Structure #1D2D50
    #38BDF8
Light mode1:
#FAF8F5
#0A192F
#E5C158
"""


class MainPage:

    def __init__(self, root):
        self.dark_mode = True
        if self.dark_mode:
            self.colors = {
                "BG": "#0E131F",
                "FG": "#38BDF8",
                "CONTRAST": "#1D2D50",
                "ENTRY": "#1E2A42",
                "FG2": "#94A3B8",
                "BUTTON": "#16357C",
                'BUTTON_FG':"#EBF1FF",
                'ACTIVE_BG':"#1A294A"
            }

        self.data_file = "expense.json"
        self.expenses = []

        self.selected_date_str = datetime.date.today().strftime("%m/%d/%Y")

        self.root = root
        self.root.resizable(width=False, height=False)
        self.root.title("Personal Expense")
        self.root.geometry("1200x720")
        self.root.configure(background=self.colors["BG"])
        self.first_frame()
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []
        else:
            self.expenses = []
        self.populate_expenses()
        self.update_dashboard()


    def populate_expenses(self):
        for exp in self.expenses:
            amt = exp.get("amount", "")
            cat = exp.get("category", "")
            dt = exp.get('date', "N/A")
            self.tree.insert("", tk.END, values=(amt, cat, dt))
    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.expenses,f, indent=2)

    def first_frame(self):
        self.font_size = 15

        # --- Left Panel ---
        frame1 = tk.Frame(self.root, bg=self.colors["CONTRAST"], width=320)
        frame1.pack(
            side=tk.LEFT, fill=tk.Y, pady=20, padx=20, ipadx=10, ipady=10
        )
        frame1.pack_propagate(False)  # Enforce fixed width for left panel

        self.adde_lbl = tk.Label(
            frame1,
            text="Add Expense",
            bg=self.colors["CONTRAST"],
            fg=self.colors["FG"],
            font=("Times New Roman", 22, "bold"),
        )
        self.adde_lbl.grid(row=0, column=1, padx=5, pady=10)
        self.amount_lbl = tk.Label(
            frame1,
            text="💰Amount",
            bg=self.colors["CONTRAST"],
            fg=self.colors["FG"],
            font=("Times New Roman", self.font_size),
        )
        self.amount_lbl.grid(row=1, column=1, padx=5, pady=10)
        self.am_sv = tk.StringVar()
        self.am_sv.set("💵")
        self.amount_entry = tk.Entry(
            frame1,
            textvariable=self.am_sv,
            bg=self.colors["ENTRY"],
            fg=self.colors["FG2"],
            font=("Times New Roman", self.font_size),justify="center"
        )
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        def del_ent(event=None):
            if self.am_sv.get() == "💵":
                self.amount_entry.delete(0, "end")

        def focus_out_ent(event=None):
            if self.am_sv.get() == "":
                self.am_sv.set("💵")

        self.amount_entry.bind("<FocusOut>", focus_out_ent)
        self.amount_entry.bind("<FocusIn>", del_ent)
        self.cate_lbl = tk.Label(
            frame1,
            text="Category",
            bg=self.colors["CONTRAST"],
            fg=self.colors["FG"],
            font=("Times New Roman", self.font_size),
        )
        self.cate_lbl.grid(row=3, column=1, padx=5, pady=10)

        categories = [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other",
        ]
        self.ctcombo_sv = tk.StringVar()
        self.categorycombo = ttk.Combobox(
            frame1,
            textvariable=self.ctcombo_sv,
            values=categories,
            state="readonly",
            font=("Times New Roman", (self.font_size - 2)),
        )
        self.categorycombo.grid(row=4, column=1, padx=5, pady=5)
        self.ctcombo_sv.set("Select Category")

        self.calendar_widget = Calendar_widget(frame1, scale=1.0, show_selected_bar=False,on_date_select=self.on_date_selected )
        self.calendar_widget.grid(row=5, column=1, padx=5, pady=(20,10))
        self.expense_add_btn = tk.Button(frame1,text="Add Expense",bg=self.colors['BUTTON'],fg=self.colors["BUTTON_FG"],activebackground=self.colors["ACTIVE_BG"],
        activeforeground=self.colors['FG2'],bd=0,font=("Times New Roman", 20, "bold"),command=self.get_info)
        self.expense_add_btn.grid(row=7, column=1, padx=5, pady=5)

        self.date_lbl = tk.Label(frame1,text=f"Date: {self.selected_date_str}",bg=self.colors["CONTRAST"],fg=self.colors["FG"],font=("Times New Roman", self.font_size))
        self.date_lbl.grid(row=6, column=1, padx=5, pady=10)




        button1_frame = tk.Frame(self.root, bg=self.colors['CONTRAST'], width=500)
        # button1_frame.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
        button1_frame.pack(side=tk.TOP, anchor="nw", pady=(20,0), padx=20)
        self.del_btn = tk.Button(button1_frame, text="Delete",bg="#FF0000",fg=self.colors["BUTTON_FG"],activebackground=self.colors["ACTIVE_BG"],
        activeforeground=self.colors['FG2'],bd=0,font=("Times New Roman", 10),command=lambda:self.delete_selected())
        self.del_btn.grid(row=0, column=2,padx=5,pady=5, ipadx=2,ipady=1)
        categories_filter = [
            "All",
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other",
        ]
        self.filter_sv = tk.StringVar()

        self.filter_combo = ttk.Combobox(button1_frame, textvariable=self.filter_sv,
        values=categories_filter,state="readonly",font=("Times New Roman", 8))
        self.filter_combo.grid(row=0, column=0, padx=5, pady=5)
        self.filter_sv.set("All")
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.update_dashboard())





        tree_frame = tk.Frame(self.root, bg=self.colors["CONTRAST"], width=300)
        tree_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0,20), padx=20, ipadx=5, ipady=5)


        self.scrollbar = ttk.Scrollbar(tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame,  columns=("Amount","Category","Date"),show='headings',height=15, yscrollcommand=self.scrollbar.set)
        self.tree.heading("Amount", text="Amount($)")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")

        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Category", width=100, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.bind("<Delete>", lambda e:self.delete_selected())

        self.tree.pack(fill=tk.BOTH, expand=True)

        chart_frame = tk.Frame(self.root, bg=self.colors["CONTRAST"], width=500)
        chart_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0,20), padx=20, ipadx=5, ipady=5)


        self.fig = Figure(figsize=(5,5), facecolor=self.colors["CONTRAST"])
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.colors["CONTRAST"])

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)








    def get_info(self):
        try:
            amount = float(self.am_sv.get())
            cate = self.ctcombo_sv.get()
            date_str = self.selected_date_str

            if cate == "Select Category"or amount <= 0:
                messagebox.showerror("Amount Error", "Please enter an amount or Select Category")

            else:
                self.tree.insert('', tk.END, values=(amount, cate, date_str))
                expense = {"amount": amount, "category": cate, "date": date_str}

                self.expenses.append(expense)
                self.save_data()

                self.am_sv.set("💵")
                self.filter_combo.set("All")
                self.amount_entry.bind("<FocusIn>", self.am_sv.set(""))
                self.ctcombo_sv.set("Select Category")
                self.update_dashboard()
        except ValueError:
            messagebox.showerror("Wrong Type", "Insert an amount")
            self.am_sv.set("")

    def on_date_selected(self, date):
        self.selected_date_str = date.strftime("%m/%d/%Y")
        self.date_lbl.config(text=f"Date: {self.selected_date_str}")
        print(self.selected_date_str)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("No Selection", "Please select an expense to delete.")
            return

        if messagebox.askyesno("Delete Expense", "Are you sure you want to delete this expense?"):
            for item in selected:
                values = self.tree.item(item)["values"]
                for expense in self.expenses:
                    if expense["amount"] == values[0] and expense["category"] == values[1] and expense["date"] == values[2]:
                        self.expenses.remove(expense)
                        break
            self.save_data()
            self.delete_all_tree()
            self.load_data()
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("No Selection", "Please select an expense to edit.")
            return
        if messagebox.askyesno("Edit Expense", "Are you sure you want to edit this expense?"):
            for item in selected:
                values = self.tree.item(item)["values"]
                for expense in self.expenses:
                    if expense["amount"] == values[0] and expense["category"] == values[1] and expense["date"] == values[2]:
                        self.am_sv.set(expense["amount"])
                        self.ctcombo_sv.set(expense["category"])
                        break
            self.save_data()
            self.delete_all_tree()
            self.load_data()
    def update_dashboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_category = self.filter_sv.get()
        filtered = self.expenses
        if filter_category != "All":
            filtered = [e for e in self.expenses if e["category"] == filter_category]

        filtered.sort(key=lambda x: x['date'], reverse=True)

        for exp in filtered:
            self.tree.insert('', tk.END, values=(exp["amount"], exp["category"], exp["date"]))

        self.plot_pie_chart(filtered)

    def plot_pie_chart(self, data):
        self.ax.clear()

        # Fix aspect ratio and axis limits so redrawing doesn't shift scales
        self.ax.set_aspect("equal")
        self.ax.set_xlim(-1.3, 1.3)
        self.ax.set_ylim(-1.3, 1.3)

        category_totals = {}
        for exp in data:
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0.0) + float(exp["amount"])

        if not category_totals or sum(category_totals.values()) == 0:
            self.wedges = []
            self.chart_data = []
            self.ax.text(
                0,
                0,
                "No Data Available",
                color=self.colors["FG2"],
                ha="center",
                va="center",
                fontsize=13,
            )
        else:
            labels = list(category_totals.keys())
            amounts = list(category_totals.values())
            total_sum = sum(amounts)

            self.chart_data = [
                (cat, amt, (amt / total_sum) * 100)
                for cat, amt in zip(labels, amounts)
            ]

            slice_colors = [
                "#38BDF8",
                "#818CF8",
                "#F472B6",
                "#34D399",
                "#FBBF24",
                "#A78BFA",
                "#F87171",
                "#4ADE80",
            ]

            # Donut chart drawing without external static text labels to prevent scaling bugs
            # self.wedges, _, autotexts = self.ax.pie(
            #     amounts,
            #     labels=None,
            #     autopct="%1.1f%%",
            #     startangle=140,
            #     colors=slice_colors[: len(labels)],
            #     pctdistance=0.72,
            #     wedgeprops=dict(width=0.4, edgecolor=self.colors["CONTRAST"], linewidth=2),
            # )
            label_iterator = iter(labels)

            self.wedges, _, autotexts = self.ax.pie(
                amounts,
                labels=None,
                autopct=lambda pct: next(
                    label_iterator
                ),  # <--- Replaces percent with category label
                startangle=140,
                colors=slice_colors[: len(labels)],
                pctdistance=0.72,
                wedgeprops=dict(width=0.4, edgecolor=self.colors["CONTRAST"], linewidth=2),
            )

            for autotext in autotexts:
                autotext.set_color("#FFFFFF")
                autotext.set_weight("bold")
                autotext.set_fontsize(9)

            for autotext in autotexts:
                autotext.set_color("#FFFFFF")
                autotext.set_weight("bold")
                autotext.set_fontsize(9)

            self.ax.set_title(
                "Expense Distribution",
                color=self.colors["FG"],
                fontsize=14,
                fontweight="bold",
                pad=10,
            )

            # Floating Tooltip Annotation Setup
            self.annot = self.ax.annotate(
                "",
                xy=(0, 0),
                xytext=(15, 15),
                textcoords="offset points",
                bbox=dict(
                    boxstyle="round,pad=0.5",
                    fc=self.colors["ENTRY"],
                    ec=self.colors["FG"],
                    lw=1,
                ),
                color="#FFFFFF",
                fontsize=10,
            )
            self.annot.set_visible(False)

        self.fig.tight_layout()
        self.canvas.draw()

    def on_hover(self, event):
        """Show floating labels when hovering over chart slices."""
        if not self.wedges or self.annot is None:
            return

        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            for i, wedge in enumerate(self.wedges):
                cont, _ = wedge.contains(event)
                if cont:
                    cat, amt, pct = self.chart_data[i]
                    self.annot.xy = (event.xdata, event.ydata)
                    self.annot.set_text(f"{cat}\n${amt:,.2f} ({pct:.1f}%)")
                    self.annot.set_visible(True)
                    self.canvas.draw_idle()
                    return

        if vis:
            self.annot.set_visible(False)
            self.canvas.draw_idle()


    def delete_all_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        return(self.tree)


class Calendar_widget(tk.Frame):

    def __init__(
        self,
        parent,
        scale=1.0,
        show_selected_bar=True,
        on_date_select=None,
        initial_date=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg="#0E131F",
            highlightbackground="#94A3B8",
            highlightthickness=max(1, int(1 * scale)),
            **kwargs,
        )

        self.scale = scale
        self.show_selected_bar = show_selected_bar
        self.on_date_select = on_date_select
        self.displayed_date = initial_date or datetime.date.today()
        self.selected_date = self.displayed_date
        self.year = self.displayed_date.year
        self.month = self.displayed_date.month

        # Compact metric scaling
        self.header_font_size = max(8, int(10 * scale))
        self.day_font_size = max(7, int(8 * scale))
        self.footer_font_size = max(7, int(8 * scale))
        self.btn_width = max(2, int(3 * scale))
        self.btn_height = 1
        self.pad_outer = max(2, int(6 * scale))
        self.pad_inner = 1

        self.configure(padx=self.pad_outer, pady=self.pad_outer)

        self._create_header()
        self._create_grid()
        if self.show_selected_bar:
            self._create_footer()

        self.update_calendar()

    def _create_header(self):
        header_frame = tk.Frame(self, bg= "#1E2A42")
        header_frame.pack(fill="x", pady=(0, int(4 * self.scale)))

        btn_prev = tk.Button(
            header_frame,
            text="◄",
            command=self._prev_month,
            relief="flat",
            bg= "#1E2A42",
            activebackground="#e5e5ea",
            bd=0,
            width=max(2, int(2 * self.scale)),
            cursor="hand2",
            font=("Segoe UI", self.day_font_size),
        )
        btn_prev.pack(side="left")

        self.lbl_month_year = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", self.header_font_size, "bold"),
            bg= "#1E2A42",
            fg="#94A3B8",
        )
        self.lbl_month_year.pack(side="left", expand=True)

        btn_next = tk.Button(
            header_frame,
            text="►",
            command=self._next_month,
            relief="flat",
            bg= "#1E2A42",
            activebackground="#94A3B8",
            bd=0,
            width=max(2, int(2 * self.scale)),
            cursor="hand2",
            font=("Segoe UI", self.day_font_size),
        )
        btn_next.pack(side="right")

    def _create_grid(self):
        self.grid_frame = tk.Frame(self, bg= "#1E2A42")
        self.grid_frame.pack()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            lbl = tk.Label(
                self.grid_frame,
                text=day,
                font=("Times New Roman", self.day_font_size, "bold"),
                fg="#94A3B8",
                bg= "#1E2A42",
                width=self.btn_width,
            )
            lbl.grid(row=0, column=col, pady=(0, int(2 * self.scale)))

    def _create_footer(self):
        self.footer_frame = tk.Frame(self, bg= "#1E2A42")
        self.footer_frame.pack(fill="x", pady=(int(4 * self.scale), 0))

        self.lbl_selected = tk.Label(
            self.footer_frame,
            text="",
            font=("Times New Roman", self.footer_font_size, "bold"),
            bg= "#1E2A42",
            fg="#94A3B8",
            pady=int(2 * self.scale),
        )
        self.lbl_selected.pack()

    def update_calendar(self):
        for widget in self.grid_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        self.lbl_month_year.config(
            text=f"{calendar.month_name[self.month]} {self.year}"
        )

        if self.show_selected_bar and hasattr(self, "lbl_selected"):
            formatted_date = self.selected_date.strftime("%A, %B %d, %Y")
            self.lbl_selected.config(text=f"Selected: {formatted_date}")

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.year, self.month)
        today = datetime.date.today()

        for r_idx, week in enumerate(month_days, start=1):
            for c_idx, day in enumerate(week):
                if day == 0:
                    continue

                current_day_date = datetime.date(self.year, self.month, day)
                is_selected = current_day_date == self.selected_date
                is_today = current_day_date == today

                if is_selected:
                    bg_col, fg_col = "#111D34", "#94A3B8"
                elif is_today:
                    bg_col, fg_col = "#606D87", "#ffffff"
                else:
                    bg_col, fg_col = "#2C3E61", "#ADB4C0"

                btn = tk.Button(
                    self.grid_frame,
                    text=str(day),
                    width=self.btn_width,
                    height=self.btn_height,
                    relief="flat",
                    bg=bg_col,
                    fg=fg_col,
                    activebackground="#0051a8",
                    activeforeground="#ffffff",
                    font=("Times New Roman", self.day_font_size),
                    cursor="hand2",
                    command=lambda d=day: self._select_day(d),
                )
                btn.grid(
                    row=r_idx,
                    column=c_idx,
                    padx=self.pad_inner,
                    pady=self.pad_inner,
                )

    def _prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def _next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

    def _select_day(self, day):
        self.selected_date = datetime.date(self.year, self.month, day)
        self.update_calendar()
        if self.on_date_select:
            self.on_date_select(self.selected_date)
        return self.selected_date


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()