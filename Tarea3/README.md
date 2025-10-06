
# Tarea 3 — Sistema de Pedidos de Comida con Concurrencia (Versión Modular)

**Autor:** Christopher Obando - C05610  
**Lenguaje:** Python 3.8+
**Repositorio** [Repositorio de github](https://github.com/ChristopherObando/software-design-II-2025)
---

## Cómo ejecutar
1. Asegúrate de tener esta estructura de archivos:
   ```
   .
   ├─ main.py
   └─ src/
      ├─ pedidos.py
      ├─ fabricas.py
      └─ servicio.py
   ```
2. Ejecuta:
   ```bash
   python main.py
   ```

Verás una salida similar a (el orden puede variar por la concurrencia):
```text
[COCINERO 1] Preparando pedido 0 (Hamburguesa)
[COCINERO 2] Preparando pedido 1 (Hamburguesa)
[COCINERO 1] Pedido 0 listo: Hamburguesa 0 preparada
[COCINERO 2] Pedido 1 listo: Hamburguesa 1 preparada
[COCINERO 1] Preparando pedido 2 (Hamburguesa)
[COCINERO 2] Preparando pedido 3 (Pizza)
[COCINERO 2] Pedido 3 listo: Pizza 3 preparada
[COCINERO 1] Pedido 2 listo: Hamburguesa 2 preparada
[COCINERO 1] Preparando pedido 4 (Pizza)
[COCINERO 1] Pedido 4 listo: Pizza 4 preparada
[SISTEMA] Todos los pedidos procesados
```

> **Nota:** la intercalación de logs puede diferir en cada ejecución por el paralelismo. Se respeta el formato de los mensajes del enunciado.

---

## Estructura de archivos
- `src/pedidos.py` — Dominio: `Pedido` (abstracta), `PedidoHamburguesa`, `PedidoPizza`.
- `src/fabricas.py` — Patrón Factory Method: `CreadorPedidos`, `CreadorHamburguesas`, `CreadorPizzas`.
- `src/servicio.py` — Concurrencia: `ServicioPedidos` con hilos (cocineros) + `queue.Queue` (thread-safe).
- `main.py` — Punto de entrada que respeta el *main esperado* del enunciado; encola 3 hamburguesas y 2 pizzas.

---

## Decisiones de diseño

### 1) Concurrencia con hilos + cola thread-safe
- Se usa `queue.Queue` como **cola segura para threads** (múltiples productores/consumidores sin condiciones de carrera).
- Cada cocinero es un `threading.Thread` que ejecuta `_worker`, consumiendo de la cola hasta recibir un **sentinel** (`None`).
- Se emplean `Queue.task_done()` y `Queue.join()` para esperar a que **todos** los pedidos terminen antes de finalizar.
- La sincronización provista por `Queue` evita bloqueos y *race conditions* sin necesidad de `Lock` manual.

### 2) Patrón Factory Method
- `CreadorPedidos` define la interfaz `crear_pedido`.
- `CreadorHamburguesas` y `CreadorPizzas` crean `PedidoHamburguesa` y `PedidoPizza` respectivamente (**polimorfismo**).
- `ServicioPedidos` no conoce clases concretas; opera contra la abstracción `Pedido`. Esto permite **agregar nuevos tipos** sin tocar la lógica de procesamiento (OCP).

### 3) Estructura y extensibilidad
- `Pedido` es abstracta y cada subclase implementa `preparar()` con su propio tiempo/flujo simulado.
- Los hilos se **nombran** como `COCINERO 1..N` para coincidir con el formato de *logs* pedido.
- Los **IDs** se reciben desde `main.py`. Si se requiere una secuencia global, puede manejarse en el *main* sin modificar `ServicioPedidos`.

