from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from libro import Libro, Genero


# ---------- Estrategia de popularidad (OCP) ----------

class ReglaPopularidad(ABC):
    @abstractmethod
    def calcular(self, libro: Libro) -> float:
        ...


class ReglaPopularidadPorDefecto(ReglaPopularidad):
    def calcular(self, libro: Libro) -> float:
        return 10.0


class ReglaPopularidadNovela(ReglaPopularidad):
    def calcular(self, libro: Libro) -> float:
        return 50 + (libro.paginas / 10)


class ReglaPopularidadCiencia(ReglaPopularidad):
    def calcular(self, libro: Libro) -> float:
        return 70 + (libro.paginas / 5)


class ReglaPopularidadHistoria(ReglaPopularidad):
    def calcular(self, libro: Libro) -> float:
        return 40 + (libro.paginas / 8)


REGLAS_POR_DEFECTO: Dict[Genero, ReglaPopularidad] = {
    Genero.NOVELA: ReglaPopularidadNovela(),
    Genero.CIENCIA: ReglaPopularidadCiencia(),
    Genero.HISTORIA: ReglaPopularidadHistoria(),
}


def calcular_popularidad(
    libro: Libro,
    reglas: Optional[Dict[Genero, ReglaPopularidad]] = None
) -> float:
    reglas = reglas or REGLAS_POR_DEFECTO
    regla = reglas.get(libro.genero, ReglaPopularidadPorDefecto())
    return regla.calcular(libro)


# ---------- Antigüedad (función simple) ----------

def es_antiguo(
    libro: Libro,
    anios_para_antiguo: int = 45,
    anio_actual: Optional[int] = None
) -> bool:
    from datetime import date
    y = anio_actual or date.today().year
    return (y - libro.anio_publicacion) >= anios_para_antiguo


# ---------- Presentación (fuera de la entidad) ----------

def imprimir_libro(
    libro: Libro,
    reglas: Optional[Dict[Genero, ReglaPopularidad]] = None,
    anios_para_antiguo: int = 45
) -> None:
    pop = calcular_popularidad(libro, reglas)
    antiguo = es_antiguo(libro, anios_para_antiguo)
    print(f"Título: {libro.titulo}")
    print(f"Autor: {libro.autor}")
    print(f"Género: {libro.genero.value}")
    print(f"Páginas: {libro.paginas}")
    print(f"Año: {libro.anio_publicacion}")
    print(f"Disponible: {'Sí' if libro.disponible else 'No'}")
    print(f"Popularidad: {pop:.2f}")
    print(f"Es antiguo: {'Sí' if antiguo else 'No'}")
    print("------------------------")


# ---------- DTO de Resumen (retorno único) ----------

class Resumen:
    def __init__(self, total: int, disponibles: int, antiguos: int, promedio_popularidad: float) -> None:
        self.total = total
        self.disponibles = disponibles
        self.antiguos = antiguos
        self.promedio_popularidad = promedio_popularidad


# ---------- Colección / Servicio de reporte ----------

class Biblioteca:
    def __init__(self) -> None:
        self._libros: List[Libro] = []

    def agregar_libro(self, libro: Libro) -> None:
        self._libros.append(libro)

    def libros(self) -> List[Libro]:
        # devolver copia para no exponer la lista interna
        return list(self._libros)

    # Entrada interactiva con validación mínima
    def agregar_libro_interactivo(self) -> None:
        try:
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            genero_txt = input("Género (novela/ciencia/historia): ").strip().lower()
            genero = parse_genero(genero_txt)

            paginas = int(input("Número de páginas: ").strip())
            if paginas <= 0:
                print("Número de páginas inválido. Se usará 1 como mínimo.")
                paginas = 1

            anio = int(input("Año de publicación: ").strip())
            if anio < 1400 or anio > 2100:
                print("Año fuera de rango razonable. Se usará 2000 por defecto.")
                anio = 2000

            self._libros.append(Libro(titulo, autor, genero, paginas, anio))
            print("Libro agregado!")
        except ValueError:
            print("Entrada inválida. No se agregó el libro.")

    # Cálculo puro (sin imprimir), retorna un objeto Resumen
    def generar_resumen(
        self,
        reglas: Optional[Dict[Genero, ReglaPopularidad]] = None,
        anios_para_antiguo: int = 45
    ) -> Resumen:
        total = len(self._libros)
        if total == 0:
            return Resumen(0, 0, 0, 0.0)

        disponibles = 0
        antiguos = 0
        pop_total = 0.0

        for libro in self._libros:
            if libro.disponible:
                disponibles += 1
            if es_antiguo(libro, anios_para_antiguo):
                antiguos += 1
            pop_total += calcular_popularidad(libro, reglas)

        promedio = pop_total / total
        return Resumen(total, disponibles, antiguos, promedio)

    # Presentación separada: detalle + resumen
    def imprimir_detalle_y_reporte(
        self,
        reglas: Optional[Dict[Genero, ReglaPopularidad]] = None,
        anios_para_antiguo: int = 45
    ) -> None:
        for libro in self._libros:
            imprimir_libro(libro, reglas, anios_para_antiguo)

        resumen = self.generar_resumen(reglas, anios_para_antiguo)
        print("\nREPORTE BIBLIOTECA:")
        print(f"Total libros: {resumen.total}")
        print(f"Disponibles: {resumen.disponibles}")
        print(f"Antiguos: {resumen.antiguos}")
        print(f"Promedio de popularidad: {resumen.promedio_popularidad:.2f}")

    # Alias por compatibilidad con el nombre del profe
    def generar_reporte(self) -> None:
        self.imprimir_detalle_y_reporte()


# ---------- Helpers ----------

def parse_genero(texto: str) -> Genero:
    if texto == "novela":
        return Genero.NOVELA
    if texto == "ciencia":
        return Genero.CIENCIA
    if texto == "historia":
        return Genero.HISTORIA
    return Genero.OTRO


# ---------- Demo rápida (opcional) ----------

if __name__ == "__main__":
    biblioteca = Biblioteca()
    biblioteca.agregar_libro(Libro("El Quijote", "Cervantes", Genero.NOVELA, 863, 1605))
    biblioteca.agregar_libro(Libro("Breve historia del tiempo", "Stephen Hawking", Genero.CIENCIA, 256, 1988))
    biblioteca.agregar_libro(Libro("Historia de Roma", "Theodor Mommsen", Genero.HISTORIA, 700, 1854))
    biblioteca.agregar_libro(Libro("Poesías", "Rubén Darío", Genero.OTRO, 120, 1896))
    biblioteca.generar_reporte()
