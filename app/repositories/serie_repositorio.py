from app.db.local import BancoDeDadosLocal


class SerieRepositorio:
    def __init__(self, database: BancoDeDadosLocal) -> None:
        self.db = database