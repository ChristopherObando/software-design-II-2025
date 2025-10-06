
"""
main.py
Autor: Christopher Obando - C05610
Python >= 3.8
"""
# Intentamos importar con paquete 'src'. Si falla, agregamos 'src' al sys.path
try:
    from src.servicio import ServicioPedidos
    from src.fabricas import CreadorHamburguesas, CreadorPizzas
except ModuleNotFoundError:
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
    from servicio import ServicioPedidos
    from fabricas import CreadorHamburguesas, CreadorPizzas

if __name__ == "__main__":
    servicio = ServicioPedidos()  # Por defecto 2 cocineros

    # Factory para hamburguesas
    creador_hamburguesas = CreadorHamburguesas()
    for i in range(3):
        pedido = creador_hamburguesas.crear_pedido(i)
        servicio.agregar_pedido(pedido)

    # TODO: Agregar otro factory para pizzas
    # Ejemplo: dos pizzas adicionales
    creador_pizzas = CreadorPizzas()
    for i in range(3, 5):
        servicio.agregar_pedido(creador_pizzas.crear_pedido(i))

    servicio.procesar_pedidos()
