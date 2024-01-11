import tkinter as tk
from tkinter import messagebox
from os.path import exists
import random
import pyperclip
import json as j

# ---------------------------- CLEAR ENTRIES ------------------------------- #

def clear_data():
    response = messagebox.askokcancel(title="Clear", message="Are you sure you want to clear all entries?")
    if response:
        website_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    search_website = website_entry.get()
    if len(search_website) == 0:
        messagebox.showinfo(title="Incomplete Data", message="Please fill all the necessary details")
    else:
        try:
            with open("data_json.json", "r") as searchable_file:
                searchable_data = j.load(searchable_file)
                try:
                    messagebox.showinfo(title="Password Details",
                                        message=f"Website: {search_website}\nUsername: {searchable_data[search_website]["usernames"]}\nPassword: {searchable_data[search_website]["passwords"]}")
                except KeyError:
                    messagebox.showinfo(title="Not Found", message=f"No data pertaining to {search_website}.")
        except FileNotFoundError:
            messagebox.showinfo(title="Empty File", message="No data saved.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_password():
    random_password_list = []
    random_password_str = ""
    small_lets = random.randint(3, 5)
    for i in range(small_lets):
        random_password_list.append(chr(random.randint(ord('A'), ord('Z'))))
    for small_num in range(8 - small_lets):
        random_password_list.append(chr(random.randint(ord('a'), ord('z'))))
    small_lets = random.randint(3, 5)
    for k in range(small_lets):
        random_password_list.append(chr(random.randint(ord('0'), ord('9'))))
    for number in range(8 - small_lets):
        ran = random.choice([[33, 47], [58, 64], [91, 96], [123, 126]])
        random_password_list.append(chr(random.randint(ran[0], ran[1])))
    random.shuffle(random_password_list)
    for elem in random_password_list:
        random_password_str += elem
    # Copies the password generated to the clipboard of the system in use
    pyperclip.copy(random_password_str)
    password_entry.delete(0, 'end')
    password_entry.insert(0, random_password_str)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Incomplete Data", message="Please dont leave any of the fields empty")
    else:
        # Confirmation Pop Up
        is_ok = messagebox.askokcancel(title="Confirm Username and Password",
                                       message=f"Website: {website}\nUsername: {username}\nPassword: {password}")
        if is_ok:
            new_data = {
                website: {
                    "usernames": username,
                    "passwords": password
                }
            }
            print(new_data)
            if not (exists("data_json.json")):
                with open("data_json.json", "w") as write_new:
                    j.dump(new_data, write_new, indent=4)
            else:
                with open("data_json.json", "r") as readable:
                    temp_data = j.load(readable)
                    temp_data.update(new_data)

                with open("data_json.json", "w") as writeable:
                    j.dump(temp_data, writeable, indent=4)

            # Clear the text-boxes
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.minsize(width=470, height=300)

# Image
canvas = tk.Canvas(height=200, width=200)
lock = tk.PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=lock)
canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

password_label = tk.Label(text="Password")
password_label.grid(row=3, column=0)

email_label = tk.Label(text="Email/Username")
email_label.grid(row=2, column=0)

# Entry
email_entry = tk.Entry(width=55)
email_entry.insert(0, "yash.testboi@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = tk.Entry(width=36)
password_entry.grid(row=3, column=1)

website_entry = tk.Entry(width=55)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2)

# Buttons
generate_button = tk.Button(text="Generate Password", command=random_password)
generate_button.grid(row=3, column=2)

add_button = tk.Button(text="Add Password", width=30, command=add_password)
add_button.grid(row=4, column=1)

search_button = tk.Button(text="Search", width=15, command=search_password)
search_button.grid(row=1, column=2)

clear_button = tk.Button(text="Clear", width=15, command=clear_data)
clear_button.grid(row=4, column=2)

window.mainloop()
