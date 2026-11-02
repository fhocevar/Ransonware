# Keylogger Lab — DIO

Laboratório educacional para estudar eventos de teclado, diferenças entre captura local e global, isolamento entre aplicações e mitigação de riscos.

## Componentes

- `keylogger/global_monitor.py`: observa eventos de teclado quando o backend permite, **sem registrar caracteres**.
- `keylogger/event_store.py`: grava timestamp, tipo e contador no CSV.
- `tests/test_keylogger_event_store.py`: testes automatizados independentes da interface gráfica.
- `docs/KEYLOGGER_LAB.md`: documentação técnica completa.

Os módulos anteriores `keylogger/simulator.py`, `login_demo.py` e `collector.py` podem ser mantidos; este pacote não os substitui.

## Instalação e testes

```bash
cd ~/projetos/python-malware-simulation-lab
source .venv/bin/activate
python -m pip install -r requirements-keylogger.txt
python -m pytest -v tests/test_keylogger_event_store.py
```

## Monitor global de atividade

```bash
python -m keylogger.global_monitor --max-events 30
```

O monitor registra somente metadados no arquivo `keylogger/logs/global_events.csv`. Em Wayland, o compositor pode bloquear a observação global. Não há captura de conteúdo de outros aplicativos, execução oculta ou exfiltração.

Leia [a documentação técnica](docs/KEYLOGGER_LAB.md) para arquitetura, exemplos, testes, riscos e critérios de aceitação.
