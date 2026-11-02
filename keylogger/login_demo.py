
from __future__ import annotations

import tkinter as tk

from keylogger.collector import Collector


def main():
    root = tk.Tk()
    root.title("DIO - Aplicação de Login Fictícia")
    root.geometry("480x370")

    collector = Collector(root)

    tk.Label(
        root,
        text="APLICAÇÃO DE TESTE - DIO",
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    tk.Label(
        root,
        text=(
            "Ambiente fictício de treinamento.\n"
            "Não utilize credenciais reais."
        ),
        fg="darkred",
    ).pack(pady=5)

    tk.Label(root, text="Usuário fictício:").pack(pady=(15, 5))

    username = tk.Entry(root, width=35)
    username.pack()
    username.bind(
        "<KeyPress>",
        lambda event: collector.capture("usuario", event),
    )

    tk.Label(root, text="Senha fictícia:").pack(pady=(15, 5))

    password = tk.Entry(root, width=35, show="*")
    password.pack()
    password.bind(
        "<KeyPress>",
        lambda event: collector.capture("senha_demo", event),
    )

    status = tk.StringVar(value="Aguardando dados fictícios")

    def submit():
        status.set("Login fictício enviado - nenhuma autenticação real")

    tk.Button(
        root,
        text="Entrar (simulação)",
        command=submit,
        width=22,
    ).pack(pady=18)

    tk.Label(
        root,
        textvariable=status,
        wraplength=400,
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
