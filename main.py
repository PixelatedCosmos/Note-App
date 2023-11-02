import tkinter as tk
from functions import createTable, addButton, deleteButton, refresh, getNoteContent, updateNoteContent

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.setup_ui()

    def setup_ui(self):
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.notesList = tk.Listbox(self.paned_window)
        self.notesList.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        self.notesContent = tk.Text(self.paned_window)
        self.notesContent.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")

        self.paned_window.add(self.notesList)
        self.paned_window.add(self.notesContent)

        self.add_button = tk.Button(self.root, text="Add", width=5, command=self.add_button_click)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", width=5, command=lambda: deleteButton(self.notesList))
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        createTable()
        refresh(self.notesList)

        self.notesList.bind("<ButtonRelease-1>", lambda event: self.displaySelectedNoteContent())
        self.notesContent.bind("<KeyRelease>", self.autoSaveContent)

    def autoSaveContent(self, event):
        selectedIndex = self.notesList.curselection()

        if selectedIndex:
            selectedTitle = self.notesList.get(selectedIndex)
            modifiedContent = self.notesContent.get("1.0", tk.END)

            updateNoteContent(selectedTitle, modifiedContent)

    def add_button_click(self):
        addButton(self.notesList)

    def displaySelectedNoteContent(self):
        selectedIndex = self.notesList.curselection()

        if selectedIndex:
            selectedTitle = self.notesList.get(selectedIndex)
            content = getNoteContent(selectedTitle)
            self.notesContent.delete("1.0", tk.END)
            self.notesContent.insert(tk.END, content)

def main():
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
