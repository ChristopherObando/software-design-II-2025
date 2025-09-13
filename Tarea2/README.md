# Tarea 2 – Refactorización de Código

**Curso:** CI-0136 Diseño de Software – II Ciclo 2025  
**Estudiante:** Christopher Obando Salgado
**Código refactorizado:** `src/libro.py`, `src/biblioteca.py`  

---

## Índice
1. [Problemas identificados](#1-problemas-identificados)  
2. [Soluciones implementadas](#2-soluciones-implementadas)  
3. [Buenas prácticas aplicadas](#3-buenas-prácticas-aplicadas)  
4. [Explicación técnica de mejoras significativas](#4-explicación-técnica-de-mejoras-significativas)  

---

1\. Problemas identificados
---------------------------

### 1.1 Biblioteca.generar\_reporte() mezcla cálculo y presentación (SRP)

*   **Descripción:** El método calcula métricas (totales, antiguos, disponibles, promedio de popularidad) y además imprime detalles y el reporte final.
    
*   **Dónde se ve:** Recorre self.libros, llama l.imprimir\_datos() (presentación) y acumula contadores/sumas (cálculo).
    
*   **Impacto:** Dificulta pruebas unitarias (hay que capturar stdout), acopla a la consola y vuelve frágil el formato de salida.
    
*   **Principio afectado:** **SRP** (y roza **DIP** si se quisiera inyectar un “renderer”).

    

### 1.2 SRP en Libro (entidad hace demasiado)

*   **Descripción:** Libro almacena datos, calcula popularidad, decide antigüedad y además imprime.
    
*   **Dónde se ve:** Métodos calcular\_popularidad, es\_antiguo e imprimir\_datos dentro de la misma clase.
    
*   **Impacto:** Aumenta el acoplamiento, dificulta el testeo aislado del dominio y complica cambios de formato de salida.
    
*   **Principio afectado:** **SRP** (y potencialmente **OCP** al querer extender reglas).

    

### 1.3 Género como “string mágico”

*   **Descripción:** genero es texto libre (“novela”, “ciencia”, “historia”) sin lista cerrada ni validación.
    
*   **Dónde se ve:** En Libro.\_\_init\_\_ y en calcular\_popularidad mediante if/elif con literales.
    
*   **Impacto:** Propenso a errores de tipeo, ramales condicionales crecen, y para nuevos géneros hay que modificar código existente.
    
*   **Principio afectado:** **OCP** (extender sin modificar) y robustez.

    

### 1.4 Acoplamiento a la consola (I/O “hardcodeado”)

*   **Descripción:** El sistema depende de input() y print() en clases de dominio/servicio.
    
*   **Dónde se ve:** Biblioteca.agregar\_libro() (usa input()), Libro.imprimir\_datos() y Biblioteca.generar\_reporte() (usan print()).
    
*   **Impacto:** Baja testabilidad, difícil reutilizar en otras interfaces (web/GUI/API) y fuerte acoplamiento a la consola.
    
*   **Principio afectado:** **DIP** (Inversión de Dependencias).
    

### 1.5 Sin validación de entradas

*   **Descripción:** No se validan paginas, anio\_publicacion ni genero; int(input()) puede lanzar ValueError.
    
*   **Dónde se ve:** Conversión directa en Biblioteca.agregar\_libro() y ausencia de validaciones en Libro.\_\_init\_\_.
    
*   **Impacto:** Fallos en ejecución, datos inconsistentes (páginas negativas, años irreales) y mala experiencia de usuario.
    
*   **Principio afectado:** Invariantes de dominio (robustez/calidad).
    
    

### 1.6 Variable temporal poco expresiva (l)

*   **Descripción:** Uso de l en lugar de nombres claros para elementos de la colección.
    
*   **Dónde se ve:** for l in self.libros:
    
*   **Impacto:** Menor legibilidad y mayor costo cognitivo al mantener/depurar.
    
*   **Principio afectado:** Estilo/legibilidad
    

## 2. Soluciones implementadas

### 2.1 Separación de cálculo y presentación (SRP)

-   **Qué se cambio:** extraigo el cálculo del reporte a `Biblioteca.generar_resumen(...) -> Resumen` (sin `print`); y dejo toda la salida en `Biblioteca.imprimir_detalle_y_reporte(...)`.
    
-   **Resultado:** ahora puedo probar números sin capturar `stdout` y reutilizar la lógica en otra UI (CLI/Web/API).
    

```python
# Cálculo puro (retorna un objeto)
def generar_resumen(self, reglas=None, anios_para_antiguo=45) -> Resumen:
    # ...recorre self._libros y computa métricas...
    return Resumen(total, disponibles, antiguos, pop_total / total)

# Presentación separada
def imprimir_detalle_y_reporte(self, reglas=None, anios_para_antiguo=45):
    for libro in self._libros:
        imprimir_libro(libro, reglas, anios_para_antiguo)
    res = self.generar_resumen(reglas, anios_para_antiguo)
    print("\nREPORTE BIBLIOTECA:"); print(f"Total libros: {res.total}")

```

----------

### 2.2 SRP en `Libro`: impresión fuera de la entidad

-   **Qué se cambio:** `Libro` queda como **modelo de datos** (sin I/O ni reglas). La salida está en `imprimir_libro(...)`.
    
-   **Resultado:** cambiar el formato de impresión no toca la entidad.
    

```python
def imprimir_libro(libro, reglas=None, anios_para_antiguo=45):
    pop = calcular_popularidad(libro, reglas)
    antiguo = es_antiguo(libro, anios_para_antiguo)
    print(f"Título: {libro.titulo}");  # ...

```

----------

### 2.3 Enum + Estrategia de popularidad (OCP)

-   **Qué se cambio:** `Genero` como `Enum` reemplaza strings mágicos; uso **Estrategia** por género y un mapa-dispatcher.
    
-   **Resultado:** agregar un género implica **añadir** una clase-regla y registrarla, sin modificar el núcleo.
    

```python
class Genero(Enum): NOVELA="novela"; CIENCIA="ciencia"; HISTORIA="historia"; OTRO="otro"

REGLAS_POR_DEFECTO = {
  Genero.NOVELA: ReglaPopularidadNovela(),
  Genero.CIENCIA: ReglaPopularidadCiencia(),
  Genero.HISTORIA: ReglaPopularidadHistoria(),
}

def calcular_popularidad(libro, reglas=None):
    reglas = reglas or REGLAS_POR_DEFECTO
    return reglas.get(libro.genero, ReglaPopularidadPorDefecto()).calcular(libro)

```

----------

### 2.4 Validación mínima en la entrada

-   **Qué se cambio:** manejo de `ValueError`, mínimos/rangos razonables y `parse_genero`.
    
-   **Resultado:** menos fallos en ejecución y datos con invariantes básicos.
    

```python
try:
    paginas = int(input("Número de páginas: ").strip())
    if paginas <= 0: paginas = 1
    anio = int(input("Año de publicación: ").strip())
    if anio < 1400 or anio > 2100: anio = 2000
except ValueError:
    print("Entrada inválida. No se agregó el libro."); return

```

----------

### 2.5 Antigüedad como función simple

-   **Qué se cambio:** `es_antiguo(libro, anios_para_antiguo=45, anio_actual=None)`.
    
-   **Resultado:** simple, parametrizable y testeable.
    

```python
def es_antiguo(libro, anios_para_antiguo=45, anio_actual=None):
    from datetime import date
    y = anio_actual or date.today().year
    return (y - libro.anio_publicacion) >= anios_para_antiguo

```

----------

### 2.6 Legibilidad: `l` → `libro`

-   **Qué se cambio:** nombres expresivos en bucles.
    
-   **Resultado:** lectura y mantenimiento más claros.
    

```python
for libro in self._libros:
    imprimir_libro(libro, reglas, anios_para_antiguo)

```

----------

## 3. Buenas prácticas aplicadas

-   **SRP (Responsabilidad Única):**
    
    -   `Libro` solo datos; la impresión vive fuera (`imprimir_libro`).
        
    -   Cálculo (`generar_resumen`) separado de la salida (`imprimir_detalle_y_reporte`).
        
-   **OCP (Abierto/Cerrado):**
    
    -   Estrategias de popularidad por género; agregar un género no requiere modificar el código existente del cálculo.
        
-   **DIP (Inversión de Dependencias, suavizado):**
    
    -   La lógica de negocio no depende de `print/input`; la vista es intercambiable.
        
-   **Evitar strings mágicos:**
    
    -   `Enum Genero` + `parse_genero` centralizan y validan los valores aceptados.
        
-   **Funciones puras y testabilidad:**
    
    -   `generar_resumen`, `calcular_popularidad`, `es_antiguo` no tienen side-effects.
        
-   **Validación de datos:**
    
    -   Manejo básico de errores y rangos razonables.
        
-   **Legibilidad:**
    
    -   Nombres claros y funciones con propósito único.
        

----------

## 4. Explicación técnica de mejoras significativas

### 4.1 Separación de cálculo y presentación (SRP + testabilidad)

-   **Antes:** `generar_reporte()` hacía cómputo y `print()` juntos.
    
-   **Después:** `generar_resumen(...) -> Resumen` computa sin I/O; `imprimir_detalle_y_reporte(...)` solo imprime.
    
-   **Por qué es mejor:**
    
    -   Permite **tests** de números sin capturar `stdout`.
        
    -   Facilita **portar a otra UI** sin tocar la lógica.
        
    -   Reduce acoplamiento, cumple **SRP**.
        

### 4.2 Enum `Genero` + Estrategia de popularidad (OCP)

-   **Antes:** `if/elif` por cadenas con riesgo de typos y difícil de extender.
    
-   **Después:** `Genero` como `Enum` y `ReglaPopularidad*` con un **dispatcher**.
    
-   **Por qué es mejor:**
    
    -   **OCP real:** nuevos géneros = nuevas reglas registradas, sin romper lo existente.
        
    -   Aísla la variación de negocio en clases pequeñas y testeables.
        
    -   Elimina strings mágicos.
        

### 4.3 DTO `Resumen` (retorno único semántico)

-   **Antes:** retorno de varios valores “sueltos”.
    
-   **Después:** un **objeto `Resumen`** con `total`, `disponibles`, `antiguos`, `promedio_popularidad`.
    
-   **Por qué es mejor:**
    
    -   Satisface la guía del profe (“un solo retorno”).
        
    -   Da **semántica** y **estabilidad** de firma (puedo añadir campos sin romper llamadas).
        

### 4.4 Antigüedad como función simple (parametrizable)

-   **Antes:** criterio fijo incrustado en la entidad.
    
-   **Después:** `es_antiguo(libro, anios_para_antiguo=45, anio_actual=None)` como función pura.
    
-   **Por qué es mejor:**
    
    -   **Simplicidad** y **flexibilidad** (cambio de política sin tocar clases).
        
    -   Fácil de **testear** (inyecto `anio_actual`).
        
    -   Si en el futuro crece la complejidad, se puede migrar a una estrategia/clase sin afectar la API actual.
        

----------