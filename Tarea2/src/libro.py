class Libro:
    def __init__(self, titulo, autor, genero, paginas, anio_publicacion, 
disponible=True):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero  # 'novela', 'ciencia', 'historia'
        self.paginas = paginas
        self.anio_publicacion = anio_publicacion
        self.disponible = disponible
    
    def calcular_popularidad(self):
        if self.genero == 'novela':
            base = 50
            extra = self.paginas / 10
        elif self.genero == 'ciencia':
            base = 70
            extra = self.paginas / 5
        elif self.genero == 'historia':
            base = 40
            extra = self.paginas / 8
        else:
            base = 10
            extra = 0
        return base + extra
    
    def es_antiguo(self):
        if self.anio_publicacion < 1980:
            return True
        else:
            return False
    
    def imprimir_datos(self):
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Género: {self.genero}")
        print(f"Páginas: {self.paginas}")
        print(f"Año: {self.anio_publicacion}")
        print(f"Disponible: {'Sí' if self.disponible else 'No'}")
        print(f"Popularidad: {self.calcular_popularidad()}")
        print(f"Es antiguo: {'Sí' if self.es_antiguo() else 'No'}")
        print("------------------------")