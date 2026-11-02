
"""
DIO - Monitor Global de Teclado
Laboratório educacional de cibersegurança.

Monitora eventos globais de teclado quando permitidos pelo
ambiente gráfico. Não registra caracteres ou senhas.
"""

from __future__ import annotations

import argparse
import csv
import os
import signal
from datetime import datetime
from pathlib import Path

from pynput import keyboard


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "global_events.csv"


class GlobalKeyboardMonitor:
    def __init__(self, max_events: int = 100):
        self.max_events = max_events
        self.count = 0
        self.running = True

    def on_press(self, _key):
        if not self.running:
            return False

        self.count += 1

        timestamp = datetime.now().isoformat(
            timespec="milliseconds"
        )

        with LOG_FILE.open(
            "a",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                "KEY_PRESS",
                self.count
            ])

        print(
            f"[{timestamp}] "
            f"Evento detectado | Total: {self.count}",
            flush=True
        )

        if self.count >= self.max_events:
            self.running = False
            return False

    def stop(self, *_args):
        self.running = False
        return False

    def run(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open(
            "w",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "event_type",
                "event_number"
            ])

        session = os.environ.get(
            "XDG_SESSION_TYPE",
            "unknown"
        )

        print("=" * 55)
        print("DIO - MONITOR GLOBAL DE TECLADO")
        print("=" * 55)
        print(f"Sessão gráfica: {session}")
        print(f"Limite de eventos: {self.max_events}")
        print(f"Arquivo de log: {LOG_FILE}")
        print("Captura de conteúdo: desativada")
        print("Interromper: Ctrl+C")
        print("=" * 55)

        if session == "wayland":
            print(
                "[AVISO] Wayland pode impedir a "
                "observação global de eventos."
            )

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        try:
            with keyboard.Listener(
                on_press=self.on_press
            ) as listener:
                listener.join()

        except Exception as exc:
            print(
                f"[ERRO] Monitoramento indisponível: {exc}"
            )

        finally:
            print(
                f"\n[FINALIZADO] "
                f"{self.count} eventos detectados."
            )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor global educacional"
    )

    parser.add_argument(
        "--max-events",
        type=int,
        default=100
    )

    args = parser.parse_args()

    if not 1 <= args.max_events <= 10000:
        parser.error(
            "--max-events deve estar entre 1 e 10000"
        )

    monitor = GlobalKeyboardMonitor(
        max_events=args.max_events
    )

    monitor.run()


if __name__ == "__main__":
    main()
