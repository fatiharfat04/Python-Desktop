import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, ttk
import os
import re
from datetime import datetime

class AdvancedTextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Text Editor")
        self.window.geometry("900x700")
        self.window.configure(bg="white")

        # File management variables
        self.current_file = None
        self.is_modified = False
        self.recent_files = []
        self.max_recent_files = 10

        # Editor settings
        self.current_font = ("Consolas", 12)
        self.word_wrap = True
        self.show_line_numbers = True

        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []

        # Setup Komponen
        self.buat_interface()
        self.buat_toolbar_buttons()
        self.buat_menu_system()
        self.bind_events()
        self.update_title()
        self.update_status("Ready")

    # ==================== INTERFACE & SYSTEM MENU ====================
    def buat_interface(self):
        # Toolbar Frame
        self.toolbar = tk.Frame(self.window, bg="lightgray", relief=tk.RAISED, bd=1)
        self.toolbar.pack(fill=tk.X)

        # Main editor frame
        editor_frame = tk.Frame(self.window)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Line numbers frame (optional/placeholder)
        self.line_numbers_frame = tk.Frame(editor_frame, bg="lightgray", width=50)

        # Text area dengan scrollbar
        self.text_area = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD if self.word_wrap else tk.NONE,
            undo=True,
            font=self.current_font,
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="lightblue"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = tk.Frame(self.window, relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Status bar labels
        self.status_label = tk.Label(
            self.status_bar, 
            text="Ready", 
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.position_label = tk.Label(
            self.status_bar, 
            text="Line: 1, Column: 1", 
            anchor=tk.E,
            font=("Arial", 9)
        )
        self.position_label.pack(side=tk.RIGHT, padx=5)

        self.file_info_label = tk.Label(
            self.status_bar, 
            text="Untitled", 
            anchor=tk.CENTER,
            font=("Arial", 9)
        )
        self.file_info_label.pack(side=tk.RIGHT, padx=20)

    def buat_toolbar_buttons(self):
        """Method untuk membuat tombol-tombol di toolbar"""
        btn_new = tk.Button(
            self.toolbar, text="📄 New", command=self.new_file,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)

        btn_open = tk.Button(
            self.toolbar, text="📁 Open", command=self.open_file,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)

        btn_save = tk.Button(
            self.toolbar, text="💾 Save", command=self.save_file,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_save.pack(side=tk.LEFT, padx=2, pady=2)

        separator1 = tk.Frame(self.toolbar, width=2, bg="gray", relief=tk.SUNKEN, bd=1)
        separator1.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        btn_undo = tk.Button(
            self.toolbar, text="↶ Undo", command=self.undo_action,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_undo.pack(side=tk.LEFT, padx=2, pady=2)

        btn_redo = tk.Button(
            self.toolbar, text="↷ Redo", command=self.redo_action,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_redo.pack(side=tk.LEFT, padx=2, pady=2)

        separator2 = tk.Frame(self.toolbar, width=2, bg="gray", relief=tk.SUNKEN, bd=1)
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        btn_find = tk.Button(
            self.toolbar, text="🔍 Find", command=self.show_find_dialog,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_find.pack(side=tk.LEFT, padx=2, pady=2)

        btn_font = tk.Button(
            self.toolbar, text="🔤 Font", command=self.change_font,
            relief=tk.FLAT, bg="lightgray", font=("Arial", 9)
        )
        btn_font.pack(side=tk.LEFT, padx=2, pady=2)

    def buat_menu_system(self):
        """Method untuk membuat menu system lengkap"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()

        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self.update_recent_menu()

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo_action, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo_action, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Find...", command=self.show_find_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace...", command=self.show_replace_dialog, accelerator="Ctrl+H")

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        self.wrap_var = tk.BooleanVar(value=self.word_wrap)
        view_menu.add_checkbutton(
            label="Word Wrap", 
            variable=self.wrap_var, 
            command=self.toggle_word_wrap
        )

        self.line_numbers_var = tk.BooleanVar(value=self.show_line_numbers)
        view_menu.add_checkbutton(
            label="Show Line Numbers", 
            variable=self.line_numbers_var, 
            command=self.toggle_line_numbers
        )
        view_menu.add_separator()
        view_menu.add_command(label="Change Font...", command=self.change_font)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Word Count", command=self.show_word_count)
        tools_menu.add_command(label="Character Count", command=self.show_char_count)
        tools_menu.add_separator()
        tools_menu.add_command(label="Insert Date/Time", command=self.insert_datetime)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    # ==================== HELPERS & STATE MANAGEMENT ====================
    def on_text_change(self, event=None):
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
        self.window.after(10, self.update_cursor_position)

    def on_cursor_move(self, event=None):
        self.window.after(10, self.update_cursor_position)

    def update_cursor_position(self):
        try:
            cursor_pos = self.text_area.index(tk.INSERT)
            line, column = cursor_pos.split('.')
            self.position_label.config(text=f"Line: {line}, Column: {int(column)+1}")
        except Exception:
            pass

    def update_title(self):
        title = "Advanced Text Editor - "
        if self.current_file:
            title += os.path.basename(self.current_file)
            self.file_info_label.config(text=os.path.basename(self.current_file))
        else:
            title += "Untitled"
            self.file_info_label.config(text="Untitled")

        if self.is_modified:
            title += " *"

        self.window.title(title)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.window.after(3000, lambda: self.status_label.config(text="Ready"))

    def confirm_save(self):
        if not self.is_modified:
            return True

        response = messagebox.askyesnocancel(
            "Save Changes",
            "Do you want to save changes to the current document?"
        )

        if response:
            return self.save_file()
        elif response is False:
            return True
        else:
            return False

    def on_closing(self):
        if self.confirm_save():
            self.window.destroy()

    # ==================== FILE OPERATIONS ====================
    def new_file(self):
        if self.is_modified:
            if not self.confirm_save():
                return
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.is_modified = False
        self.update_title()
        self.update_status("New file created")

    def open_file(self):
        if self.is_modified:
            if not self.confirm_save():
                return
        file_types = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("JavaScript files", "*.js"),
            ("HTML files", "*.html"),
            ("CSS files", "*.css"),
            ("JSON files", "*.json"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=file_types
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.current_file = filename
                self.is_modified = False
                self.add_to_recent_files(filename)
                self.update_title()
                self.update_status(f"Opened: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.is_modified = False
                self.update_title()
                self.update_status(f"Saved: {os.path.basename(self.current_file)}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
                return False
        else:
            return self.save_as_file()

    def save_as_file(self):
        file_types = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("JavaScript files", "*.js"),
            ("HTML files", "*.html"),
            ("CSS files", "*.css"),
            ("JSON files", "*.json"),
            ("All files", "*.*")
        ]
        filename = filedialog.asksaveasfilename(
            title="Save As",
            filetypes=file_types,
            defaultextension=".txt"
        )
        if filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = filename
                self.is_modified = False
                self.add_to_recent_files(filename)
                self.update_title()
                self.update_status(f"Saved as: {os.path.basename(filename)}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
                return False
        return False

    # ==================== RECENT FILES ====================
    def add_to_recent_files(self, filename):
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        self.update_recent_menu()

    def update_recent_menu(self):
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="No recent files", state=tk.DISABLED)
        else:
            for i, filename in enumerate(self.recent_files):
                display_name = os.path.basename(filename)
                if len(display_name) > 30:
                    display_name = display_name[:27] + "..."
                self.recent_menu.add_command(
                    label=f"{i+1}. {display_name}",
                    command=lambda f=filename: self.open_recent_file(f)
                )
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label="Clear Recent Files",
                command=self.clear_recent_files
            )

    def open_recent_file(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File not found: {filename}")
            self.recent_files.remove(filename)
            self.update_recent_menu()
            return
        if self.is_modified:
            if not self.confirm_save():
                return
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
            self.current_file = filename
            self.is_modified = False
            self.add_to_recent_files(filename)
            self.update_title()
            self.update_status(f"Opened: {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {str(e)}")

    def clear_recent_files(self):
        if messagebox.askyesno("Clear Recent Files", "Clear all recent files from the list?"):
            self.recent_files.clear()
            self.update_recent_menu()

    # ==================== EDIT OPERATIONS ====================
    def undo_action(self):
        try:
            self.text_area.edit_undo()
            self.update_status("Undo performed")
        except tk.TclError:
            self.update_status("Nothing to undo")

    def redo_action(self):
        try:
            self.text_area.edit_redo()
            self.update_status("Redo performed")
        except tk.TclError:
            self.update_status("Nothing to redo")

    def cut_text(self):
        try:
            self.text_area.event_generate("<<Cut>>")
            self.update_status("Text cut to clipboard")
        except Exception:
            self.update_status("Cannot cut text")

    def copy_text(self):
        try:
            self.text_area.event_generate("<<Copy>>")
            self.update_status("Text copied to clipboard")
        except Exception:
            self.update_status("Cannot copy text")

    def paste_text(self):
        try:
            self.text_area.event_generate("<<Paste>>")
            self.update_status("Text pasted from clipboard")
        except Exception:
            self.update_status("Cannot paste text")

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.update_status("All text selected")

    # ==================== FIND & REPLACE ====================
    def show_find_dialog(self):
        self.find_dialog = tk.Toplevel(self.window)
        self.find_dialog.title("Find")
        self.find_dialog.geometry("400x150")
        self.find_dialog.transient(self.window)
        self.find_dialog.grab_set()

        tk.Label(self.find_dialog, text="Find:").pack(pady=5)
        self.find_entry = tk.Entry(self.find_dialog, width=40)
        self.find_entry.pack(pady=5)
        self.find_entry.focus()

        options_frame = tk.Frame(self.find_dialog)
        options_frame.pack(pady=5)
        self.case_sensitive_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Case sensitive", variable=self.case_sensitive_var).pack(side=tk.LEFT, padx=5)
        self.whole_word_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Whole word", variable=self.whole_word_var).pack(side=tk.LEFT, padx=5)

        buttons_frame = tk.Frame(self.find_dialog)
        buttons_frame.pack(pady=10)
        tk.Button(buttons_frame, text="Find Next", command=self.find_next, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Find All", command=self.find_all, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Close", command=self.find_dialog.destroy, width=10).pack(side=tk.LEFT, padx=5)

        self.find_entry.bind("<Return>", lambda e: self.find_next())

    def find_next(self):
        search_text = self.find_entry.get()
        if not search_text:
            return

        start_pos = self.text_area.index(tk.INSERT)
        case_sensitive = self.case_sensitive_var.get()

        pos = self.text_area.search(search_text, start_pos, tk.END, nocase=not case_sensitive)
        if pos:
            end_pos = f"{pos}+{len(search_text)}c"
            self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
            self.text_area.tag_add(tk.SEL, pos, end_pos)
            self.text_area.mark_set(tk.INSERT, end_pos)
            self.text_area.see(pos)
            self.update_status(f"Found: {search_text}")
        else:
            pos = self.text_area.search(search_text, "1.0", start_pos, nocase=not case_sensitive)
            if pos:
                end_pos = f"{pos}+{len(search_text)}c"
                self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_area.tag_add(tk.SEL, pos, end_pos)
                self.text_area.mark_set(tk.INSERT, end_pos)
                self.text_area.see(pos)
                self.update_status(f"Found: {search_text} (wrapped)")
            else:
                messagebox.showinfo("Find", f"'{search_text}' not found")

    def find_all(self):
        search_text = self.find_entry.get()
        if not search_text:
            return

        self.text_area.tag_remove("found", "1.0", tk.END)
        start_pos = "1.0"
        count = 0
        while True:
            pos = self.text_area.search(
                search_text, start_pos, tk.END, nocase=not self.case_sensitive_var.get()
            )
            if not pos:
                break
            end_pos = f"{pos}+{len(search_text)}c"
            self.text_area.tag_add("found", pos, end_pos)
            count += 1
            start_pos = end_pos

        self.text_area.tag_config("found", background="yellow", foreground="black")
        if count > 0:
            self.update_status(f"Found {count} occurrences of '{search_text}'")
        else:
            messagebox.showinfo("Find All", f"'{search_text}' not found")

    def show_replace_dialog(self):
        self.replace_dialog = tk.Toplevel(self.window)
        self.replace_dialog.title("Replace")
        self.replace_dialog.geometry("400x200")
        self.replace_dialog.transient(self.window)
        self.replace_dialog.grab_set()

        tk.Label(self.replace_dialog, text="Find:").pack(pady=5)
        self.replace_find_entry = tk.Entry(self.replace_dialog, width=40)
        self.replace_find_entry.pack(pady=5)

        tk.Label(self.replace_dialog, text="Replace with:").pack(pady=5)
        self.replace_with_entry = tk.Entry(self.replace_dialog, width=40)
        self.replace_with_entry.pack(pady=5)
        self.replace_find_entry.focus()

        options_frame = tk.Frame(self.replace_dialog)
        options_frame.pack(pady=5)
        self.replace_case_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Case sensitive", variable=self.replace_case_var).pack(side=tk.LEFT, padx=5)

        buttons_frame = tk.Frame(self.replace_dialog)
        buttons_frame.pack(pady=10)
        tk.Button(buttons_frame, text="Replace", command=self.replace_current, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(buttons_frame, text="Replace All", command=self.replace_all, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(buttons_frame, text="Close", command=self.replace_dialog.destroy, width=12).pack(side=tk.LEFT, padx=2)

    def replace_current(self):
        find_text = self.replace_find_entry.get()
        replace_text = self.replace_with_entry.get()
        if not find_text:
            return

        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            if (self.replace_case_var.get() and selected_text == find_text) or \
               (not self.replace_case_var.get() and selected_text.lower() == find_text.lower()):
                self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.insert(tk.INSERT, replace_text)
                self.update_status(f"Replaced: {find_text} -> {replace_text}")
            else:
                messagebox.showinfo("Replace", "No matching text selected")
        except tk.TclError:
            messagebox.showinfo("Replace", "No text selected")

    def replace_all(self):
        find_text = self.replace_find_entry.get()
        replace_text = self.replace_with_entry.get()
        if not find_text:
            return

        content = self.text_area.get("1.0", tk.END)
        if self.replace_case_var.get():
            new_content = content.replace(find_text, replace_text)
            count = content.count(find_text)
        else:
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            new_content = pattern.sub(replace_text, content)
            count = len(pattern.findall(content))

        if count > 0:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            self.update_status(f"Replaced {count} occurrences")
            messagebox.showinfo("Replace All", f"Replaced {count} occurrences of '{find_text}'")
        else:
            messagebox.showinfo("Replace All", f"'{find_text}' not found")

    # ==================== VIEW & TOOLS ====================
    def toggle_word_wrap(self):
        self.word_wrap = self.wrap_var.get()
        self.text_area.config(wrap=tk.WORD if self.word_wrap else tk.NONE)
        self.update_status(f"Word wrap {'enabled' if self.word_wrap else 'disabled'}")

    def toggle_line_numbers(self):
        self.show_line_numbers = self.line_numbers_var.get()
        self.update_status(f"Line numbers {'enabled' if self.show_line_numbers else 'disabled'}")

    def change_font(self):
        font_dialog = tk.Toplevel(self.window)
        font_dialog.title("Change Font")
        font_dialog.geometry("300x200")
        font_dialog.transient(self.window)
        font_dialog.grab_set()

        tk.Label(font_dialog, text="Font Family:").pack(pady=5)
        font_families = ["Arial", "Times New Roman", "Courier New", "Consolas", "Verdana"]
        font_var = tk.StringVar(value=self.current_font[0])
        font_combo = ttk.Combobox(font_dialog, textvariable=font_var, values=font_families)
        font_combo.pack(pady=5)

        tk.Label(font_dialog, text="Font Size:").pack(pady=5)
        size_var = tk.IntVar(value=self.current_font[1])
        size_spinbox = tk.Spinbox(font_dialog, from_=8, to=72, textvariable=size_var)
        size_spinbox.pack(pady=5)

        def apply_font():
            new_font = (font_var.get(), size_var.get())
            self.current_font = new_font
            self.text_area.config(font=new_font)
            self.update_status(f"Font changed to {new_font[0]} {new_font[1]}")
            font_dialog.destroy()

        buttons_frame = tk.Frame(font_dialog)
        buttons_frame.pack(pady=20)
        tk.Button(buttons_frame, text="Apply", command=apply_font).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Cancel", command=font_dialog.destroy).pack(side=tk.LEFT, padx=5)

    def show_word_count(self):
        content = self.text_area.get("1.0", tk.END)
        words = len(content.split())
        lines = content.count('\n')
        messagebox.showinfo("Word Count", f"Words: {words}\nLines: {lines}")

    def show_char_count(self):
        content = self.text_area.get("1.0", tk.END)
        chars = len(content)
        chars_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
        messagebox.showinfo("Character Count", f"Characters: {chars}\nCharacters (no spaces): {chars_no_spaces}")

    def insert_datetime(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, current_datetime)
        self.update_status("Date/time inserted")

    def show_about(self):
        about_text = """Advanced Text Editor
Version 1.0
A feature-rich text editor built with Python Tkinter.

Features:
- File operations (New, Open, Save, Save As)
- Recent files management
- Find and Replace
- Undo/Redo
- Word wrap and line numbers
- Font customization
- Word and character count
- Date/time insertion

Created for educational purposes."""
        messagebox.showinfo("About", about_text)

    # ==================== EVENT BINDINGS ====================
    def bind_events(self):
        # File operations shortcuts
        self.window.bind('<Control-n>', lambda e: self.new_file())
        self.window.bind('<Control-o>', lambda e: self.open_file())
        self.window.bind('<Control-s>', lambda e: self.save_file())
        self.window.bind('<Control-S>', lambda e: self.save_as_file())
        self.window.bind('<Control-q>', lambda e: self.on_closing())

        # Edit operations shortcuts
        self.window.bind('<Control-z>', lambda e: self.undo_action())
        self.window.bind('<Control-y>', lambda e: self.redo_action())
        self.window.bind('<Control-x>', lambda e: self.cut_text())
        self.window.bind('<Control-c>', lambda e: self.copy_text())
        self.window.bind('<Control-v>', lambda e: self.paste_text())
        self.window.bind('<Control-a>', lambda e: self.select_all())

        # Find & replace shortcuts
        self.window.bind('<Control-f>', lambda e: self.show_find_dialog())
        self.window.bind('<Control-h>', lambda e: self.show_replace_dialog())

        # Text and cursor events
        self.text_area.bind('<<Modified>>', self.on_text_change)
        self.text_area.bind('<KeyRelease>', self.on_cursor_move)
        self.text_area.bind('<ButtonRelease-1>', self.on_cursor_move)

        # Window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def jalankan(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AdvancedTextEditor()
    app.jalankan()