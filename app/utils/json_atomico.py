import json
import os
from pathlib import Path
import tempfile


def salvar_json_atomico(caminho: Path, dados: list) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = None

    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            dir=caminho.parent,
            prefix=f'.{caminho.name}.',
            suffix='.tmp',
            delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)