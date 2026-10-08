import tkinter as tk

class KonverterSuhu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Konverter Suhu")
        self.window.geometry("520x600")
        self.window.minsize(480, 560)
        self.window.configure(bg="#F3F6FA")

        # Variabel kontrol
        self.celsius_var = tk.DoubleVar()
        self.fahrenheit_var = tk.DoubleVar()
        self.kelvin_var = tk.DoubleVar()
        self.rankine_var = tk.DoubleVar()

        # Flag untuk mencegah infinite loop saat update
        self.updating = False

        self.buat_interface()
        self.setup_traces()

    def buat_interface(self):
        background = "#F3F6FA"
        foreground = "#1F2937"

        header = tk.Frame(self.window, bg=background)
        header.pack(fill=tk.X, padx=28, pady=(24, 18))

        tk.Label(
            header,
            text="Konverter Suhu",
            font=("Segoe UI", 21, "bold"),
            fg="#173B67",
            bg=background
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Konversi suhu dengan mudah ke berbagai skala",
            font=("Segoe UI", 10),
            fg="#667085",
            bg=background
        ).pack(anchor="w", pady=(4, 0))

        main_frame = tk.Frame(self.window, bg=background)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=28, pady=(0, 24))

        tk.Label(
            main_frame,
            text="MASUKKAN NILAI SUHU",
            font=("Segoe UI", 9, "bold"),
            fg="#667085",
            bg=background
        ).pack(anchor="w", pady=(0, 8))

        input_card = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground="#DCE3EC",
            highlightthickness=1
        )
        input_card.pack(fill=tk.X)

        fields = (
            ("Celsius", "°C", self.celsius_var, "celsius_entry"),
            ("Fahrenheit", "°F", self.fahrenheit_var, "fahrenheit_entry"),
            ("Kelvin", "K", self.kelvin_var, "kelvin_entry"),
            ("Rankine", "°R", self.rankine_var, "rankine_entry"),
        )

        for index, (name, unit, variable, entry_name) in enumerate(fields):
            row = tk.Frame(input_card, bg="white")
            row.pack(fill=tk.X, padx=14, pady=5)

            tk.Label(
                row,
                text=f"{name} ({unit})",
                font=("Segoe UI", 11, "bold"),
                fg=foreground,
                bg="white",
                anchor="w"
            ).pack(side=tk.LEFT, padx=(4, 12), pady=7)

            entry = tk.Entry(
                row,
                textvariable=variable,
                font=("Segoe UI", 12),
                fg=foreground,
                bg="#F8FAFC",
                insertbackground=foreground,
                width=16,
                justify="right",
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground="#DCE3EC",
                highlightcolor="#3B82F6"
            )
            entry.pack(side=tk.RIGHT, padx=4, pady=3, ipady=7)
            setattr(self, entry_name, entry)

            if index < len(fields) - 1:
                tk.Frame(input_card, bg="#EEF2F6", height=1).pack(
                    fill=tk.X,
                    padx=16
                )

        info_frame = tk.Frame(main_frame, bg="#EAF2FC")
        info_frame.pack(fill=tk.X, pady=(16, 14))

        tk.Label(
            info_frame,
            text="INFORMASI SUHU",
            font=("Segoe UI", 9, "bold"),
            fg="#315B8A",
            bg="#EAF2FC"
        ).pack(anchor="w", padx=14, pady=(11, 2))

        self.info_label = tk.Label(
            info_frame,
            text="Masukkan nilai suhu pada salah satu kolom.",
            font=("Segoe UI", 10),
            fg="#344054",
            bg="#EAF2FC",
            justify=tk.LEFT,
            anchor="w",
            wraplength=420
        )
        self.info_label.pack(fill=tk.X, padx=14, pady=(0, 12))

        tk.Button(
            main_frame,
            text="Reset Semua",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#315B8A",
            activeforeground="white",
            activebackground="#254A73",
            relief=tk.FLAT,
            cursor="hand2",
            padx=18,
            pady=8,
            command=self.reset_all
        ).pack(anchor="e")

    def setup_traces(self):
        """Setup trace untuk semua variabel"""
        self.celsius_var.trace_add("write", self.from_celsius)
        self.fahrenheit_var.trace_add("write", self.from_fahrenheit)
        self.kelvin_var.trace_add("write", self.from_kelvin)
        self.rankine_var.trace_add("write", self.from_rankine)

    def from_celsius(self, *args):
        """Konversi dari Celsius ke skala lain"""
        if self.updating:
            return

        try:
            celsius = self.celsius_var.get()
            self.updating = True

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = (celsius + 273.15) * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            # Terjadi saat input tidak valid (kosong atau bukan angka)
            pass
        except Exception as e:
            self.updating = False

    def from_fahrenheit(self, *args):
        """Konversi dari Fahrenheit ke skala lain"""
        if self.updating:
            return

        try:
            fahrenheit = self.fahrenheit_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = (fahrenheit - 32) * 5/9
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = fahrenheit + 459.67
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_kelvin(self, *args):
        """Konversi dari Kelvin ke skala lain"""
        if self.updating:
            return

        try:
            kelvin = self.kelvin_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Rankine
            rankine = kelvin * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_rankine(self, *args):
        """Konversi dari Rankine ke skala lain"""
        if self.updating:
            return

        try:
            rankine = self.rankine_var.get()
            self.updating = True

            # Konversi ke Kelvin
            kelvin = rankine * 5/9
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = rankine - 459.67
            self.fahrenheit_var.set(round(fahrenheit, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def reset_all(self):
        """Reset semua field"""
        self.updating = True
        self.celsius_var.set(0)
        self.fahrenheit_var.set(0)
        self.kelvin_var.set(0)
        self.rankine_var.set(0)
        self.updating = False
        self.update_info()

    def update_info(self):
        """Update informasi tambahan"""
        try:
            celsius = self.celsius_var.get()

            info_text = f"Suhu saat ini: {celsius}°C\n"

            if celsius == 0:
                info_text += "• Titik beku air (kondisi normal)"
            elif celsius == 100:
                info_text += "• Titik didih air (kondisi normal)"
            elif celsius == -273.15:
                info_text += "• Suhu absolut nol"
            elif celsius < -273.15:
                info_text += "• Di bawah suhu absolut nol (tidak mungkin)"
                info_text += "\n• Di bawah titik beku air"
            elif celsius > 100:
                info_text += "• Di atas titik didih air"
            else:
                info_text += "• Suhu normal"

            self.info_label.config(text=info_text)
        except tk.TclError:
            self.info_label.config(text="Masukkan nilai suhu yang valid")

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = KonverterSuhu()
    app.jalankan()