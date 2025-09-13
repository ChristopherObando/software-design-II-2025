from enum import Enum


class Genero(Enum):
    NOVELA = "novela"
    CIENCIA = "ciencia"
    HISTORIA = "historia"
    OTRO = "otro"


class Libro:
    """
    Entidad de dominio simple (sin I/O ni reglas de negocio).
    Mantiene SRP: sólo representa datos del libro.
    """
    def __init__(
        self,
        titulo: str,
        autor: str,
        genero: Genero,
        paginas: int,
        anio_publicacion: int,
        disponible: bool = True,
    ):
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.genero = genero
        self.paginas = paginas
        self.anio_publicacion = anio_publicacion
        self.disponible = disponible
