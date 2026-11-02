
"""
DIO - Simulador educacional de ransomware.

Comandos:
    python -m ransomware.simulator encrypt
    python -m ransomware.simulator decrypt

Opera exclusivamente com três arquivos fictícios
dentro do volume Docker /lab-data.
"""

import argparse
import hashlib
import hmac
import os
import stat
from pathlib import Path
from getpass import getpass

from cryptography.fernet import Fernet, InvalidToken


ROOT = Path("/lab-data")
SAMPLES = ROOT / "samples"
ENCRYPTED = ROOT / "encrypted"
RECOVERED = ROOT / "recovered"

KEY_FILE = ROOT / "lab.key"
NOTE_FILE = ENCRYPTED / "RANSOM_NOTE.txt"

SAMPLE_DATA = {
    "documento.txt": "Documento fictício para teste de segurança.",
    "financeiro.txt": "Dados financeiros simulados. Nenhum dado real.",
    "clientes.txt": "Alice, Bob, Carlos - usuários fictícios.",
}

MAX_BYTES = 4096


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_environment() -> None:
    if ROOT.is_symlink() or not ROOT.is_dir():
        raise RuntimeError(
            "Volume /lab-data indisponível. Execute no Docker."
        )

    for directory in (SAMPLES, ENCRYPTED, RECOVERED):
        if directory.is_symlink():
            raise RuntimeError("Link simbólico não permitido.")

        directory.mkdir(mode=0o700, exist_ok=True)

        if not directory.is_dir():
            raise RuntimeError("Diretório inválido.")


def exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def read_file(path: Path) -> bytes:
    """Lê apenas arquivos regulares pequenos, sem seguir symlinks."""
    fd = os.open(
        path,
        os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
    )

    try:
        info = os.fstat(fd)

        if not stat.S_ISREG(info.st_mode):
            raise RuntimeError(f"Arquivo inválido: {path.name}")

        if info.st_size > MAX_BYTES:
            raise RuntimeError(f"Arquivo muito grande: {path.name}")

        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(MAX_BYTES + 1)

        if len(data) > MAX_BYTES:
            raise RuntimeError(f"Limite excedido: {path.name}")

        return data
    finally:
        os.close(fd)


def write_file(path: Path, data: bytes) -> None:
    """Cria um arquivo novo sem sobrescrever um existente."""
    fd = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )

    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


def expected_sample(name: str) -> bytes:
    return SAMPLE_DATA[name].encode("utf-8")


def prepare() -> None:
    """Cria exclusivamente os três arquivos fictícios."""
    for name in SAMPLE_DATA:
        path = SAMPLES / name

        if exists(path):
            if read_file(path) != expected_sample(name):
                raise RuntimeError(
                    f"Conteúdo inesperado em {name}."
                )
        else:
            write_file(path, expected_sample(name))
            print(f"[CRIADO] {name}")


def simulate() -> None:
    """Criptografa cópias e salva uma chave nova de laboratório."""
    check_environment()

    # Não permite substituir uma simulação anterior.
    if exists(KEY_FILE) or exists(NOTE_FILE):
        raise RuntimeError(
            "Já existe uma simulação neste volume. "
            "A chave anterior foi preservada."
        )

    for name in SAMPLE_DATA:
        if exists(ENCRYPTED / f"{name}.encrypted"):
            raise RuntimeError(
                "Arquivos criptografados já existem. "
                "Operação cancelada."
            )

    prepare()

    # Confirma que todas as entradas são os dados fictícios esperados.
    originals = {}

    for name in SAMPLE_DATA:
        data = read_file(SAMPLES / name)

        if data != expected_sample(name):
            raise RuntimeError(f"Arquivo não autorizado: {name}")

        originals[name] = data

    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted_data = {
        name: cipher.encrypt(data)
        for name, data in originals.items()
    }

    # A chave é gravada antes dos arquivos criptografados.
    write_file(KEY_FILE, key)

    for name, data in encrypted_data.items():
        write_file(ENCRYPTED / f"{name}.encrypted", data)
        print(f"[CRIPTOGRAFADO] {name}")

    note = (
        "============================================\n"
        "      SIMULAÇÃO DE RANSOMWARE - DIO\n"
        "============================================\n"
        "Seus arquivos fictícios foram criptografados.\n"
        "Para recuperá-los, informe a chave de teste.\n"
        "Nenhum pagamento é necessário.\n"
        "Nenhum arquivo pessoal foi afetado.\n"
    )

    write_file(NOTE_FILE, note.encode("utf-8"))

    print("\n" + note)
    print("[OK] Chave salva em /lab-data/lab.key")
    print("[INFO] A chave de recuperação não será exibida no terminal.")
    print("[SUCESSO] Simulação de criptografia concluída.")


def restore() -> None:
    """Solicita a chave e recupera os três arquivos fictícios."""
    check_environment()

    if not KEY_FILE.is_file() or KEY_FILE.is_symlink():
        raise RuntimeError("Arquivo lab.key não encontrado.")

    saved_key = read_file(KEY_FILE)

    print("\n========== RECUPERAÇÃO - DIO ==========")
    print("Informe a chave gerada durante a criptografia.")
    print("A digitação ficará oculta no terminal.\n")

    entered_key = None

    for attempt in range(1, 4):
        value = getpass(
            f"Chave de recuperação ({attempt}/3): "
        ).strip()

        try:
            candidate = value.encode("ascii")
            Fernet(candidate)
        except (ValueError, UnicodeEncodeError):
            print("[ERRO] Formato de chave inválido.")
            continue

        if hmac.compare_digest(candidate, saved_key):
            entered_key = candidate
            print("[OK] Chave correta!")
            break

        print("[ERRO] Chave incorreta.")

    if entered_key is None:
        print("[BLOQUEADO] Limite de tentativas atingido.")
        return

    cipher = Fernet(entered_key)
    restored_data = {}

    # Verifica tudo antes de gravar os arquivos recuperados.
    for name in SAMPLE_DATA:
        source = ENCRYPTED / f"{name}.encrypted"
        destination = RECOVERED / name

        if exists(destination):
            raise RuntimeError(
                f"Arquivo recuperado já existe: {name}"
            )

        encrypted = read_file(source)

        try:
            decrypted = cipher.decrypt(encrypted)
        except InvalidToken as exc:
            raise RuntimeError(
                f"Falha na descriptografia: {name}"
            ) from exc

        original = read_file(SAMPLES / name)

        if original != expected_sample(name):
            raise RuntimeError(
                f"Arquivo original inesperado: {name}"
            )

        if sha256(decrypted) != sha256(original):
            raise RuntimeError(
                f"Falha de integridade: {name}"
            )

        restored_data[name] = decrypted

    for name, data in restored_data.items():
        write_file(RECOVERED / name, data)
        print(f"[RECUPERADO] {name} - SHA-256 OK")

    print("\n[SUCESSO] Todos os arquivos foram recuperados!")
    print("[OK] Arquivos salvos em /lab-data/recovered")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Laboratório educacional de ransomware - DIO"
    )

    parser.add_argument(
        "action",
        choices=("encrypt", "decrypt"),
    )

    args = parser.parse_args()

    if args.action == "encrypt":
        simulate()
    else:
        restore()


if __name__ == "__main__":
    main()
