import sqlite3
from tkinter import simpledialog, messagebox, END
from datetime import datetime


def getTitle():
        titleInput = simpledialog.askstring("Input", "Enter note title:")

        if titleInput:
            return titleInput

def refresh(notesList):
    conn = sqlite3.connect("Notebook.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title from notes")
    titles = [row[0] for row in cursor.fetchall()]

    conn.close()

    notesList.delete(0, END)
    for title in titles:
        notesList.insert(END, title)

def createTable():
    conn = sqlite3.connect("Notebook.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes 
                   (noteID INTEGER PRIMARY KEY, 
                   title TEXT,
                   content TEXT,
                   creationDate DATETIME,
                   lastModifiedDate DATETIME
                   )''')
    conn.commit()
    conn.close()

def addButton(notesList):
    newTitle = getTitle()

    if newTitle:
        newCreationDate = datetime.now()
        newLastModifiedDate = datetime.now()

        try:
            conn = sqlite3.connect("Notebook.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Notes (title, content, creationDate, lastModifiedDate) VALUES (?, ?, ?, ?)",
                            (newTitle, "", newCreationDate, newLastModifiedDate))
            conn.commit()
            conn.close()

            refresh(notesList)
            messagebox.showinfo("Success", "Note added successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding the note: {e}")

def deleteButton(notesList):
    selected_index = notesList.curselection()
    
    if selected_index:
        selected_title = notesList.get(selected_index)

        try:
            conn = sqlite3.connect("Notebook.db")
            cursor = conn.cursor()
            cursor.execute("SELECT noteID FROM notes WHERE title = ?", (selected_title,))
            note_id = cursor.fetchone()

            if note_id:
                cursor.execute("DELETE FROM notes WHERE noteID = ?", (note_id[0],))
                conn.commit()

            conn.close()

            notesList.delete(selected_index)
            messagebox.showinfo("Success", "Note deleted successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting the note: {e}")



    
