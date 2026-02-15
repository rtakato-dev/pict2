```
myproject/
├─ myproject/
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ cli.py
│  └─ mylib/
│     ├─ __init__.py
│     └─ mylib.py

```

| ファイル             | 役割                                    |
| ---------------- | ------------------------------------- |
| `__main__.py`    | `python -m myproject` / exe のエントリポイント |
| `cli.py`         | CLI引数の解釈・制御                           |
| `mylib/mylib.py` | PICT実行ロジック（純粋ロジック）                    |
