import tkinter
from tkinter import *
from PIL import ImageTk
import sqlite3
import random

# Creates reusable variables for background and foreground colors.
bg_color = "#0099cc"
button_bg = "#e6f9ff"
active_bg = "#000000"
fg_color = "#ffffff"
button_fg = "#000000"
active_fg = "#e6f9ff"


def widget_clear(frame):
    # Clears old widgets from screen.
    for widget in frame.winfo_children():
        widget.destroy()


def get_db():
    # Creates connection to database of recipes.
    connection = sqlite3.connect("recipes.db")
    cursor = connection.cursor()
    # Fetches all table names using SQL commands.
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    # Randomly chooses recipe from database field.
    table_index = random.randint(0, len(all_tables) - 1)

    # Fetches ingredients list from each table.
    table_name = all_tables[table_index][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    # Closes connection and returns results of search.
    connection.close()
    return table_name, table_records


def format_text(table_name, table_records):
    # Title of random recipe and formatted text.
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    # Creates empty ingredients list.
    ingredients = []

    # List of recipe ingredients organized and formatted. Title of table and ingredients list returned.
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)

    return title, ingredients


def load_frame1():
    # Clears widgets from previous frame.
    widget_clear(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # Creates image widget.
    logo_image = ImageTk.PhotoImage(file="logo.png")
    logo_widget = tkinter.Label(frame1, image=logo_image, bg=bg_color)
    logo_widget.image = logo_image
    logo_widget.pack(pady=30)

    # Introductory widget.
    tkinter.Label(frame1, text="How about something new tonight?", bg=bg_color, fg=fg_color,
                  font=("TkMenuFont", 14)).pack(pady=30)
    # Generate random recipe button widget.
    tkinter.Button(frame1, text="Generate a recipe!", font=("TkHeadingFont", 20), bg=button_bg, fg=button_fg, cursor="question_arrow",
                   activebackground=active_bg, activeforeground=active_fg, command=lambda: load_frame2()).pack(pady=25)


def load_frame2():
    # Clears widgets from previous frame.
    widget_clear(frame1)
    frame2.tkraise()
    table_name, table_records = get_db()
    title, ingredients = format_text(table_name, table_records)
    # Creates image widget.
    logo_image = ImageTk.PhotoImage(file="recipe_plate.png")
    logo_widget = tkinter.Label(frame2, image=logo_image, bg=bg_color)
    logo_widget.image = logo_image
    logo_widget.pack(pady=20)
    # Creates font type from recipe title and ingredients list.
    tkinter.Label(frame2, text=title, bg=bg_color, fg=fg_color,
                  font=("TkHeadingFont", 20)).pack(pady=25)
    for i in ingredients:
        tkinter.Label(frame2, text=i, bg=bg_color, fg=fg_color,
                      font=("TkMenuFont", 12)).pack()

    # Back button widget.
    tkinter.Button(frame2, text="Previous Page", font=("TkHeadingFont", 18), bg=button_bg, fg=button_fg,
                   cursor="hand1", activebackground=active_bg, activeforeground=active_fg,
                   command=lambda: load_frame1()).pack(pady=25)


# Initializes program.
root = Tk()
root.title("The Traveling Chef's Recipe Generator")
root.eval("tk::PlaceWindow . center")

# Creates the widget frame.
frame1 = tkinter.Frame(root, width=500, height=600, bg=bg_color)
frame2 = tkinter.Frame(root, bg=bg_color)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="NESW")

load_frame1()

# Runs the program.
root.mainloop()
