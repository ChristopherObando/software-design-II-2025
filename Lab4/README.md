# Lab 4 — Pruebas con dobles y DI

![CI – lab4-tests](https://github.com/ChristopherObando/software-design-ii-2025/actions/workflows/tests.yml/badge.svg?branch=main)

Este laboratorio extiende la simulación de combate del curso aplicando **inyección de dependencias (DI)** y **pruebas unitarias** con dobles de prueba (`Dummy`/`Mock`) usando `unittest` y `unittest.mock`.

## ¿Qué se agregó en esta entrega?

### Nueva funcionalidad (código de producción)

- `src/models/axe.py`: arma **Axe** (Hacha) con **20** de daño base.  
  - Si la calculadora inyectada determina **golpe crítico**, el sistema suma **+10** de daño (lógica existente de `CombatSystem`).

#### Sistema elemental (Decorator)
- `src/models/elements.py`: enum de elementos (`WATER`, `FIRE`, `PLANT`, `LIGHTNING`).
- `src/models/imbued_weapon.py`: **ImbuedWeapon**, decorador que envuelve un arma y añade daño elemental.
- Cambios mínimos de integración:
  - `src/models/character.py`: soporte de estado elemental (`elements`, `apply_element`, `clear_elements`).
  - `src/app/combat_system.py`: si el arma imbuida lo indica, **se desactiva el crítico** (no se consulta la calculadora).

**Reglas:**
- Un arma imbuida siempre agrega **+5** de daño elemental.
- Las armas imbuidas **no hacen crítico**.
- Si el objetivo ya tiene un elemento **distinto**, ocurre **reacción elemental** y el bono es **+15** (triple).  
  Tras la reacción, los elementos del objetivo se **limpian**.
- Si **no** hay reacción, el elemento del arma queda **aplicado** al objetivo para futuros golpes.

**Ejemplo de uso:**
```python
from src.models.sword import Sword
from src.models.imbued_weapon import ImbuedWeapon
from src.models.elements import Element

weapon = ImbuedWeapon(Sword(), Element.LIGHTNING)

```

### Pruebas nuevas (valor real)

1.  `tests/test_axe.py`
    
    -   Verifica daño base del hacha sin crítico.
        
    -   Verifica daño con **crítico** usando `MagicMock` como calculadora (DI).
        
2.  `tests/test_combat_system_edges.py`
    
    -   Valida el **early return**: si el objetivo ya está muerto, **no** se consulta la calculadora (protege el contrato de DI con `assert_not_called()`).
        
3.  `tests/test_elemental_weapon.py`
    
    -   **Bono elemental +5** sin crítico (se usa `MagicMock` y se verifica `assert_not_called()`).
        
    -   **Reacción elemental +15** y limpieza de elementos del objetivo.
        

### CI/CD

-   Workflow de GitHub Actions: `.github/workflows/tests.yml`
    
    -   Ejecuta `python -m unittest discover -v` en **3 versiones** de Python (3.10, 3.11, 3.12).
        
    -   Configurado con `working-directory: Lab4`.
        

## Estructura principal

```
Lab4/
  src/
    app/
      combat_system.py
      damage_calculator.py
      i_combat_system.py
      i_damage_calculator.py
    models/
      character.py
      weapon.py
      sword.py
      bow.py
      axe.py                # <- NUEVO (arma)
      elements.py           # <- NUEVO (enum)
      imbued_weapon.py      # <- NUEVO (decorator)
      __init__.py
  tests/
    mocked_models/
      dummy_weapon.py
      mock_dummy_weapon.py
    test_character.py
    test_dependency_injection.py
    test_axe.py                   # <- NUEVO
    test_combat_system_edges.py   # <- NUEVO
    test_elemental_weapon.py      # <- NUEVO
.github/
  workflows/
    tests.yml

```

## Cómo ejecutar las pruebas (local)

Desde la carpeta `Lab4/`:

```bash
python -m unittest discover -v
```

Salida esperada (ejemplo):

```
Ran 9 tests in X.XXXs
OK
```

> Nota: en CI se usa `working-directory: Lab4`, por lo que no necesitas rutas adicionales.

## Dobles de prueba y DI

-   **DI**: `CombatSystem` recibe un `damage_calculator` inyectado; en pruebas empleamos **`MagicMock`** para forzar o impedir golpes críticos y **verificar llamadas** (`assert_called_once`, `assert_not_called`).
    
-   **Dummy**: `tests/mocked_models/dummy_weapon.py` ilustra un arma mínima para aislar la lógica de cálculo.
    
-   Para armas **imbuidas**, el crítico se **omite** explícitamente (y se verifica con `assert_not_called()`).
    

## Requisitos

-   Python 3.10+ (probado también en 3.11 y 3.12 en CI).
    

## Comandos útiles

```bash
# Ejecutar todos los tests
python -m unittest discover -v

# Ejecutar un archivo de test específico
python -m unittest -v tests/test_axe.py

```

## Notas de diseño

-   Se respeta **SRP**/**SOLID**: el cálculo de crítico permanece desacoplado vía interfaz; el arma define solo su daño base.
    
-   El sistema elemental usa **Decorator** (**OCP**): añadimos comportamiento sin modificar `Sword`/`Bow`.
    
-   La validación de “objetivo muerto” evita trabajo innecesario y favorece **contratos claros** con los colaboradores inyectados.