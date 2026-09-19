Personal Expense Tracker

A sleek, desktop-based personal expense management application built using Python, Tkinter, and Matplotlib. Featuring a custom embedded calendar widget, real-time data persistence, and dynamic pie chart visualization, this application provides an easy way to track and review daily expenses.

Features

Expense Logging: Add expenses with specific amounts, standard categories, and custom dates.

Custom Calendar Widget: Native Tkinter calendar component allowing fast date selection for entry logging.

Data Persistence: Expense entries are automatically stored locally in a structured JSON file (expense.json).

Interactive Data Visualization: Dynamically updated Matplotlib donut/pie chart showing categorical spending distributions with interactive tooltips.

Filtering & Management: Filter expenses by categories (Food, Bills, Transport, etc.) and delete recorded entries easily.

Modern UI: Tailored dark-themed interface built for clarity and daily ease of use.

Tech Stack

Language: Python 3.x

GUI Framework: Tkinter (with ttk widgets)

Data Visualization: Matplotlib (FigureCanvasTkAgg)

Data Format: JSON

Prerequisites

Ensure you have Python 3.8+ installed on your system.

Install the required Python packages:

pip install matplotlib


(Note: tkinter, json, datetime, calendar, and os are built into standard Python distributions.)

Usage & Installation

Clone or Download the project repository.

Ensure Personal Expense.py is in your working directory.

Run the application via terminal or command prompt:

python "Personal Expense.py"


Project Structure

.
├── Personal Expense.py  # Main application logic & Tkinter GUI
└── expense.json         # Auto-generated local storage for expense records


Key Code Overview

MainPage: Manages primary GUI frame, event bindings, treeview updates, JSON saving/loading, and Matplotlib chart integration.

Calendar_widget: Custom tk.Frame implementation handling month navigation, date rendering, and callback triggers upon date selection.

Data Schema:

[
  {
    "amount": 45.5,
    "category": "Food",
