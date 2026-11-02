
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import scrolledtext

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "keylogger_demo.log"


class KeyloggerLab:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DIO - Keylogger Educacional")
        self.root.geometry("760x540")
        self.root.minsize(600, 420)

        self.recording = False
        self.events = []

        tk.Label(
            root,
            text="LABORATÓRIO DE KEYLOGGER - DIO",
            font=("Arial", 16, "bold"),
        ).pack(pady=15)

        tk.Label(
            root,
            text=(
                "Simulação controlada: somente teclas digitadas "
                "na área abaixo são registradas.\n"
                "Não digite senhas ou informações pessoais reais."
            ),
            fg="darkred",
            justify="center",
        ).pack(pady=5)

        tk.Label(
            root,
            text="Área de digitação fictícia:",
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.input_area = scrolledtext.ScrolledText(
            root,
            height=6,
            wrap=tk.WORD,
        )
        self.input_area.pack(fill="both", expand=True, padx=20)
        self.input_area.bind("<KeyPress>", self.on_key_press)

        controls = tk.Frame(root)
        controls.pack(pady=12)

        tk.Button(
            controls,
            text="Iniciar captura",
            command=self.start,
            width=17,
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Parar captura",
            command=self.stop,
            width=17,
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Salvar log",
            command=self.save,
            width=17,
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Limpar",
            command=self.clear,
            width=12,
        ).pack(side="left", padx=5)

        self.status = tk.StringVar(value="Captura desativada")
        tk.Label(
            root,
            textvariable=self.status,
            font=("Arial", 10, "bold"),
        ).pack(pady=5)

        tk.Label(root, text="Eventos registrados:").pack(
            anchor="w", padx=20
        )

        self.output = scrolledtext.ScrolledText(
            root,
            height=8,
            state="disabled",
        )
        self.output.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    def start(self):
        self.recording = True
        self.status.set("Captura ativa - somente na área de teste")
        self.input_area.focus_set()

    def stop(self):
        self.recording = False
        self.status.set("Captura interrompida")

    def on_key_press(self, event):
        if not self.recording:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if event.keysym in ("Return", "BackSpace", "Tab", "space"):
            key = f"[{event.keysym}]"
        elif event.char and event.char.isprintable():
            key = event.char
        else:
            key = f"[{event.keysym}]"

        record = f"{timestamp} | {key}"
        self.events.append(record)

        self.output.configure(state="normal")
        self.output.insert(tk.END, record + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def save(self):
        if not self.events:
            self.status.set("Nenhum evento para salvar")
            return

        LOG_FILE.write_text(
            "\n".join(self.events) + "\n",
            encoding="utf-8",
        )
        self.status.set(f"Log salvo: {LOG_FILE}")

    def clear(self):
        self.events.clear()
        self.input_area.delete("1.0", tk.END)
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")
        self.status.set("Eventos limpos")


def main():
    root = tk.Tk()
    KeyloggerLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
