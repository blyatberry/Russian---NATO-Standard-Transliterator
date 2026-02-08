#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

from russian_nato_transliterator import (
    transliterate_auto,
    transliterate_bgn_to_ru,
    transliterate_ru_to_bgn,
)


class RussianNatoTransliteratorGUIEn:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Russian NATO Transliterator")
        self.root.geometry("1000x700")
        self.root.minsize(780, 560)
        self.style = ttk.Style(self.root)

        self.direction_var = tk.StringVar(value="auto")
        self.ascii_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Ready")
        self.font_family_var = tk.StringVar(value="Arial")
        self.font_size_var = tk.IntVar(value=11)

        self._build_ui()
        self._on_direction_changed()
        self._apply_fonts(update_status=False)

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        self.title_label = ttk.Label(
            main,
            text="Russian <-> NATO (BGN/PCGN) Transliterator",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        controls = ttk.LabelFrame(main, text="Options")
        controls.grid(row=1, column=0, sticky="ew", pady=(10, 8))
        for idx in range(11):
            controls.columnconfigure(idx, weight=1)

        ttk.Label(controls, text="Direction:").grid(
            row=0, column=0, sticky="w", padx=8, pady=6
        )
        ttk.Radiobutton(
            controls,
            text="Auto",
            variable=self.direction_var,
            value="auto",
            command=self._on_direction_changed,
        ).grid(row=0, column=1, sticky="w", padx=8, pady=6)
        ttk.Radiobutton(
            controls,
            text="RU -> LAT",
            variable=self.direction_var,
            value="ru2lat",
            command=self._on_direction_changed,
        ).grid(row=0, column=2, sticky="w", padx=8, pady=6)
        ttk.Radiobutton(
            controls,
            text="LAT -> RU",
            variable=self.direction_var,
            value="lat2ru",
            command=self._on_direction_changed,
        ).grid(row=0, column=3, sticky="w", padx=8, pady=6)

        self.ascii_check = ttk.Checkbutton(
            controls,
            text="ASCII mode (yo instead of ë)",
            variable=self.ascii_var,
        )
        self.ascii_check.grid(row=0, column=4, columnspan=2, sticky="w", padx=8, pady=6)

        ttk.Button(controls, text="Transliterate", command=self._transliterate).grid(
            row=0, column=6, sticky="e", padx=8, pady=6
        )
        ttk.Button(controls, text="Swap", command=self._swap_texts).grid(
            row=0, column=7, sticky="e", padx=8, pady=6
        )

        ttk.Label(controls, text="Font:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        font_values = self._font_families()
        self.font_family_combo = ttk.Combobox(
            controls,
            textvariable=self.font_family_var,
            values=font_values,
            state="readonly",
            width=24,
        )
        self.font_family_combo.grid(row=1, column=1, columnspan=3, sticky="ew", padx=8, pady=6)
        self.font_family_combo.bind("<<ComboboxSelected>>", self._on_font_change)

        ttk.Label(controls, text="Size:").grid(row=1, column=4, sticky="w", padx=8, pady=6)
        self.font_size_spin = ttk.Spinbox(
            controls,
            from_=8,
            to=32,
            textvariable=self.font_size_var,
            width=6,
            command=self._on_font_change,
        )
        self.font_size_spin.grid(row=1, column=5, sticky="w", padx=8, pady=6)
        self.font_size_spin.bind("<Return>", self._on_font_change)
        self.font_size_spin.bind("<FocusOut>", self._on_font_change)
        ttk.Button(controls, text="Apply font", command=self._apply_fonts).grid(
            row=1, column=6, columnspan=2, sticky="w", padx=8, pady=6
        )

        text_area = ttk.Frame(main)
        text_area.grid(row=2, column=0, sticky="nsew", pady=6)
        text_area.columnconfigure(0, weight=1)
        text_area.columnconfigure(1, weight=1)
        text_area.rowconfigure(1, weight=1)

        in_header = ttk.Frame(text_area)
        in_header.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 4))
        in_header.columnconfigure(0, weight=1)
        ttk.Label(in_header, text="Input").grid(row=0, column=0, sticky="w")
        ttk.Button(in_header, text="Load file", command=self._load_input_file).grid(
            row=0, column=1, sticky="e"
        )

        out_header = ttk.Frame(text_area)
        out_header.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 4))
        out_header.columnconfigure(0, weight=1)
        ttk.Label(out_header, text="Output").grid(row=0, column=0, sticky="w")
        ttk.Button(out_header, text="Save file", command=self._save_output_file).grid(
            row=0, column=1, sticky="e"
        )

        self.input_text = tk.Text(text_area, wrap="word", undo=True)
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        self.output_text = tk.Text(text_area, wrap="word", undo=False)
        self.output_text.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

        actions = ttk.Frame(main)
        actions.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        actions.columnconfigure(10, weight=1)

        ttk.Button(actions, text="Output -> Input", command=self._copy_output_to_input).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(actions, text="Clear", command=self._clear_texts).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(actions, text="Close", command=self.root.destroy).grid(row=0, column=2)

        ttk.Label(actions, text="(c) Developed by blyatberry").grid(
            row=0, column=9, sticky="w", padx=(8, 8)
        )
        ttk.Label(actions, textvariable=self.status_var).grid(row=0, column=10, sticky="e")

    def _font_families(self) -> list[str]:
        families = sorted(set(tkfont.families(self.root)))
        if "Arial" not in families:
            families.insert(0, "Arial")
        return families

    def _safe_font_size(self) -> int:
        try:
            size = int(self.font_size_var.get())
        except (TypeError, ValueError, tk.TclError):
            size = 11
        size = max(8, min(32, size))
        self.font_size_var.set(size)
        return size

    def _on_font_change(self, _event: object | None = None) -> None:
        self._apply_fonts(update_status=True)

    def _apply_fonts(self, update_status: bool = True) -> None:
        family = self.font_family_var.get().strip() or "Arial"
        size = self._safe_font_size()

        self.root.option_add("*Font", f"{family} {size}")
        self.style.configure("TLabel", font=(family, size))
        self.style.configure("TButton", font=(family, size))
        self.style.configure("TRadiobutton", font=(family, size))
        self.style.configure("TCheckbutton", font=(family, size))
        self.style.configure("TLabelframe.Label", font=(family, size, "bold"))

        self.title_label.configure(font=(family, size + 1, "bold"))
        self.input_text.configure(font=(family, size + 1))
        self.output_text.configure(font=(family, size + 1))

        if update_status:
            self.status_var.set("Font updated")

    def _on_direction_changed(self) -> None:
        if self.direction_var.get() == "ru2lat":
            self.ascii_check.state(["!disabled"])
        else:
            self.ascii_check.state(["disabled"])
            self.ascii_var.set(False)

    def _get_input(self) -> str:
        return self.input_text.get("1.0", tk.END).rstrip("\n")

    def _set_output(self, text: str) -> None:
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)

    def _transliterate(self) -> None:
        source = self._get_input()
        if not source:
            messagebox.showinfo("Info", "Please enter input text first.")
            return

        direction = self.direction_var.get()
        ascii_only = bool(self.ascii_var.get())

        try:
            if direction == "ru2lat":
                converted = transliterate_ru_to_bgn(source, ascii_only=ascii_only)
            elif direction == "lat2ru":
                converted = transliterate_bgn_to_ru(source)
            else:
                converted = transliterate_auto(source, ascii_only=ascii_only)
        except Exception as exc:
            messagebox.showerror("Error", f"Transliteration failed:\n{exc}")
            self.status_var.set("Failed")
            return

        self._set_output(converted)
        self.status_var.set("Done")

    def _swap_texts(self) -> None:
        source = self._get_input()
        target = self.output_text.get("1.0", tk.END).rstrip("\n")
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", target)
        self._set_output(source)
        self.status_var.set("Texts swapped")

    def _copy_output_to_input(self) -> None:
        target = self.output_text.get("1.0", tk.END).rstrip("\n")
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", target)
        self.status_var.set("Output copied")

    def _clear_texts(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("Cleared")

    def _load_input_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Load input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not read file:\n{exc}")
            return
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", content)
        self.status_var.set("File loaded")

    def _save_output_file(self) -> None:
        output = self.output_text.get("1.0", tk.END).rstrip("\n")
        if not output:
            messagebox.showinfo("Info", "Output is empty.")
            return

        path = filedialog.asksaveasfilename(
            title="Save output file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(output)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not save file:\n{exc}")
            return
        self.status_var.set("File saved")


def main() -> int:
    root = tk.Tk()
    RussianNatoTransliteratorGUIEn(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
