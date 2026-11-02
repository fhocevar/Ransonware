
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "captura_demo.log"


class Collector:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.events: list[str] = []

        self.window = tk.Toplevel(root)
        self.window.title("DIO - Coletor Educacional")
        self.window.geometry("650x440")

        tk.Label(
            self.window,
            text="COLETOR DE EVENTOS - LABORATÓRIO DIO",
            font=("Arial", 13, "bold"),
        ).pack(pady=12)

        tk.Label(
            self.window,
            text="Captura somente eventos do formulário fictício.",
            fg="darkred",
        ).pack()

        self.output = scrolledtext.ScrolledText(
            self.window,
            width=75,
            height=17,
            state="disabled",
        )
        self.output.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=12,
        )

        tk.Button(
            self.window,
            text="Salvar log",
            command=self.save,
        ).pack(pady=8)

    def capture(self, field: str, event: tk.Event):
        timestamp = datetime.now().isoformat(
            timespec="milliseconds"
        )

        if event.keysym in ("Return", "BackSpace", "Tab"):
            key = f"[{event.keysym}]"
        elif event.char and event.char.isprintable():
            key = event.char
        else:
            key = f"[{event.keysym}]"

        record = f"{timestamp} | campo={field} | tecla={key}"
        self.events.append(record)

        self.output.configure(state="normal")
        self.output.insert(tk.END, record + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def save(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(
            "\n".join(self.events) + "\n",
            encoding="utf-8",
        )

        self.output.configure(state="normal")
        self.output.insert(
            tk.END,
            f"\n[OK] Log salvo em {LOG_FILE}\n",
        )
        self.output.see(tk.END)
        self.output.configure(state="disabled")
