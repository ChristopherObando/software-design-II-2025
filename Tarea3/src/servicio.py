
"""
servicio.py
Servicio concurrente que coordina a los "cocineros" (hilos) y una cola thread-safe.
"""
from __future__ import annotations

from queue import Queue
import threading
from typing import Optional, List

from src.pedidos import Pedido

class ServicioPedidos:
    """
    Servicio que coordina la preparación de pedidos usando hilos (cocineros)
    y una cola thread-safe (Queue). Cada cocinero consume pedidos hasta
    recibir una 'señal de parada' (sentinel).
    """

    def __init__(self, num_cocineros: int = 2) -> None:
        if num_cocineros < 1:
            raise ValueError("Debe haber al menos un cocinero (hilo).")
        self._cola: Queue[Optional[Pedido]] = Queue()
        self._num_cocineros = num_cocineros
        self._hilos: List[threading.Thread] = []

    def agregar_pedido(self, pedido: Pedido) -> None:
        """Encola un pedido para ser procesado por algún cocinero."""
        self._cola.put(pedido)

    def _worker(self) -> None:
        """Función ejecutada por cada hilo cocinero."""
        nombre_cocinero = threading.current_thread().name  # p.ej. 'COCINERO 1'
        while True:
            pedido = self._cola.get()  # Bloquea hasta tener un item
            try:
                if pedido is None:
                    # Señal de parada: marcar como hecho y salir
                    self._cola.task_done()
                    break

                # Log de inicio de preparación
                print(f"[{nombre_cocinero}] Preparando pedido {pedido.id_pedido} ({pedido.tipo})", flush=True)

                # Preparar y obtener mensaje de resultado
                resultado = pedido.preparar()

                # Log de finalización
                print(f"[{nombre_cocinero}] Pedido {pedido.id_pedido} listo: {resultado}", flush=True)
            finally:
                # Importante para Queue.join()
                if pedido is not None:
                    self._cola.task_done()

    def procesar_pedidos(self) -> None:
        """
        Inicia hilos, espera a que la cola se vacíe y detiene a los cocineros.
        Imprime un log final cuando todo termina.
        """
        # Crear e iniciar los hilos con nombres predecibles
        for i in range(self._num_cocineros):
            t = threading.Thread(target=self._worker, name=f"COCINERO {i+1}", daemon=True)
            self._hilos.append(t)
            t.start()

        # Enviar un 'sentinel' (None) por cada cocinero para que se detengan
        for _ in range(self._num_cocineros):
            self._cola.put(None)

        # Esperar a que todos los items (pedidos + sentinels) sean procesados
        self._cola.join()

        # Asegurar que todos los hilos terminen
        for t in self._hilos:
            t.join(timeout=0.1)  # Pequeño timeout por seguridad

        print("[SISTEMA] Todos los pedidos procesados", flush=True)
