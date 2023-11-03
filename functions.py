import sqlite3
from tkinter import simpledialog, messagebox, END
from datetime import datetime


def getTitle():
        titleInput = simpledialog.askstring("Input", "Enter note title:")

        if titleInput:
            return titleInput

def getNoteContent(title):
    conn = sqlite3.connect("Notebook.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM notes WHERE title = ?", (title, ))
    content = cursor.fetchone()[0]
    conn.close()
    return content

def updateNoteContent(title, content):
    try:
        conn = sqlite3.connect("Notebook.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE notes SET content = ? WHERE title = ?", (content, title))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating the note content: {e}")


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

def addButton(notesList, notesContent):
    newTitle = getTitle()

    if newTitle:
        newCreationDate = datetime.now()
        newLastModifiedDate = datetime.now()

        try:
            conn = sqlite3.connect("Notebook.db")
            cursor = conn.cursor()

            # Check if the title already exists
            cursor.execute("SELECT COUNT(*) FROM notes WHERE title = ?", (newTitle,))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("INSERT INTO Notes (title, content, creationDate, lastModifiedDate) VALUES (?, ?, ?, ?)",
                               (newTitle, "", newCreationDate, newLastModifiedDate))
                conn.commit()
                conn.close()

                refresh(notesList)
                notesContent.delete("1.0", END)  # Clear the notesContent Text widget

            else:
                conn.close()
                messagebox.showerror("Error", "Note with the same title already exists.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding the note: {e}")

    return newTitle  # Return the newTitle, so you can use it in NotesApp

def deleteButton(notesList, notesContent):
    selected_index = notesList.curselection()
    
    if selected_index:
        selected_title = notesList.get(selected_index)

        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the note?")
        if confirm:
            try:
                conn = sqlite3.connect("Notebook.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM notes WHERE title = ?", (selected_title,))    

                conn.commit()
                conn.close()

                notesList.delete(selected_index)
                notesContent.delete("1.0", END)

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error deleting the note: {e}")



    
