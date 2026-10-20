import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x450")
        self.root.resizable(False, False)

        self.expression = tk.StringVar()

        display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            readonlybackground="white",
        )
        display.pack(fill="both", padx=10, pady=10, ipady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ("C", 0, 0), ("⌫", 0, 1), ("(", 0, 2), (")", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for text, row, column in buttons:
            button = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 18),
                command=lambda value=text: self.on_button_click(value),
            )
            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=3,
                pady=3,
            )

        for index in range(5):
            button_frame.rowconfigure(index, weight=1)

        for index in range(4):
            button_frame.columnconfigure(index, weight=1)

        root.bind("<Return>", lambda event: self.calculate())
        root.bind("<BackSpace>", lambda event: self.delete_last())
        root.bind("<Escape>", lambda event: self.clear())

    def on_button_click(self, value):
        if value == "C":
            self.clear()
        elif value == "⌫":
            self.delete_last()
        elif value == "=":
            self.calculate()
        else:
            self.expression.set(self.expression.get() + value)

    def clear(self):
        self.expression.set("")

    def delete_last(self):
        self.expression.set(self.expression.get()[:-1])

    def calculate(self):
        try:
            result = eval(
                self.expression.get(),
                {"__builtins__": None},
                {},
            )
            self.expression.set(str(result))
        except (SyntaxError, TypeError, ZeroDivisionError):
            self.expression.set("Error")


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()