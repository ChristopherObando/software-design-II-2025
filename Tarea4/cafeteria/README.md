# Tarea 4 – Simulación de Cafetería


-   Estudiante: Christopher Obando Salgado - C05610

## 1. Descripción general

Este proyecto implementa una **simulación de una cafetería** donde:

- Los clientes pueden ordenar **bebidas** (por ejemplo: café, té).
- Los clientes pueden ordenar **alimentos** (por ejemplo: croissant).
- Los productos se pueden **personalizar con extras** (leche, canela, crema, relleno de chocolate, etc.).
- Los pedidos se **preparan** por el personal (barista y pastelero) y luego se **notifica** a los clientes cuando sus órdenes están listas.

Además, se aplican **dos patrones de diseño** de la lista solicitada:

- `Decorator`
- `Observer`

---

## 2. Requisitos y ejecución

### Requisitos

- Python 3.10 o superior (probado con Python 3.11/3.13).

### Cómo ejecutar

Desde la carpeta raíz del proyecto (donde está `cafeteria/`):

```bash
cd cafeteria
python main.py

```

La salida esperada es similar a:

```text
=== Simulacion de Cafeteria ===
Cliente: Ana
Ordena un cafe con leche y canela
Ordena un croissant con relleno de chocolate
Cliente: Carlos
Ordena un te verde
Ordena un cafe doble espresso con crema
[Barista]: Preparo bebida: Cafe con leche y canela
[Pastelero]: Preparo alimento: Croissant con relleno de chocolate
[Barista]: Preparo bebida: Te verde
[Barista]: Preparo bebida: Cafe doble espresso con crema
[Sistema]: Se notifican los clientes cuando sus pedidos estan listos.

```

----------

## 3. Estructura del proyecto

```text
cafeteria/
  main.py            # Punto de entrada, construye la simulación
  customers.py       # Clase Customer (clientes)
  menu_items.py      # Clases base de ítems (bebida/alimento)
  decorators.py      # Extras que decoran ítems (Decorator)
  orders.py          # Order y OrderManager (gestión de pedidos)
  observer.py        # Subject, Observer, NotificationService (Observer)
  staff.py           # Barista y PastryChef que preparan pedidos
  README.md          # Este archivo

```

### Descripción breve de los módulos

-   **`customers.py`**  
    Define la clase `Customer`, que representa a una persona que hace pedidos.
    
-   **`menu_items.py`**  
    Contiene la interfaz abstracta `MenuItem` y las implementaciones concretas:
    
    -   `BasicBeverage` (bebidas base, como café, té).
        
    -   `BasicFood` (alimentos base, como croissant).
        
-   **`decorators.py`**  
    Implementa el patrón **Decorator** para los extras:
    
    -   Decorador base: `ExtraDecorator`.
        
    -   Decoradores concretos: `Milk`, `Cinnamon`, `Cream`, `ChocolateFilling`.
        
-   **`orders.py`**  
    Define:
    
    -   `Order`: une un `Customer` con un `MenuItem`.
        
    -   `OrderManager`: almacena los pedidos y hereda de `Subject` (patrón Observer).
        
-   **`observer.py`**  
    Implementa el patrón **Observer**:
    
    -   `Observer`: interfaz de observador.
        
    -   `Subject`: mantiene la lista de observadores y los notifica.
        
    -   `NotificationService`: observador concreto que imprime mensajes del sistema.
        
-   **`staff.py`**  
    Simula al personal de la cafetería:
    
    -   `Barista`: prepara bebidas.
        
    -   `PastryChef`: prepara alimentos.
        
-   **`main.py`**  
    Orquesta toda la simulación:
    
    -   Crea clientes y pedidos.
        
    -   Aplica decoradores para agregar extras.
        
    -   Asigna pedidos a `Barista` o `PastryChef`.
        
    -   Al finalizar, usa Observer para notificar que los pedidos están listos.
        

----------

## 4. Patrones de diseño utilizados

### 4.1. Patrón Decorator

**Objetivo**

Permitir que una bebida o alimento se pueda **extender dinámicamente** con extras (leche, canela, crema, relleno de chocolate) sin tener que crear una clase diferente para cada combinación posible (por ejemplo, `CafeConLecheYCanela`, `CafeConCrema`, etc.).

**Implementación**

-   Interfaz / componente base: `MenuItem` (`menu_items.py`).
    
-   Componentes concretos:
    
    -   `BasicBeverage`
        
    -   `BasicFood`
        
-   Decorador base: `ExtraDecorator` (`decorators.py`).
    
-   Decoradores concretos:
    
    -   `Milk`
        
    -   `Cinnamon`
        
    -   `Cream`
        
    -   `ChocolateFilling`
        

Cada decorador:

-   Recibe un `MenuItem` en el constructor.
    
-   Delegan el método `cost()` en el componente base y agregan un costo adicional.
    
-   Extienden la descripción con texto como “con leche”, “y canela”, etc.
    

**Ejemplo de uso (en `main.py`)**

```python
coffee = BasicBeverage("Cafe", 1200.0)
coffee = Milk(coffee)
coffee = Cinnamon(coffee)
print(coffee.description())  # "Cafe con leche y canela"

```

**Justificación**

-   Evita explosión de clases para cada combinación de extras.
    
-   Es fácil agregar nuevos extras sin modificar las clases existentes (**principio Open/Closed**).
    
-   Permite reutilizar lógica de costo, categoría y descripción de manera flexible.
    

----------

### 4.2. Patrón Observer

**Objetivo**

Separar la **lógica de preparación de pedidos** de la **forma en que el sistema notifica eventos** (por ejemplo, informar que todos los pedidos están listos). La idea es que el sistema pueda tener varios observadores (notificación por consola, envío de correo, etc.) sin acoplar directamente la lógica de pedidos a cada forma de notificación.

**Implementación**

En `observer.py`:

-   `Subject`:
    
    -   Mantiene una lista de `Observer`.
        
    -   Métodos: `attach`, `detach`, `notify`.
        
-   `Observer`:
    
    -   Interfaz con el método `update(message: str)`.
        
-   `NotificationService`:
    
    -   Implementación concreta de `Observer`.
        
    -   En `update`, imprime mensajes con el formato `[Sistema]: ...`.
        

En `orders.py`:

-   `OrderManager` hereda de `Subject`:
    
    -   Guarda todos los pedidos (`_orders`).
        
    -   Puede notificar a los observadores cuando los pedidos se hayan procesado.
        

En `main.py`:

```python
order_manager = OrderManager()
notification_service = NotificationService()
order_manager.attach(notification_service)

# ... se construyen y procesan los pedidos ...

order_manager.notify("Se notifican los clientes cuando sus pedidos estan listos.")

```

**Justificación**

-   Permite agregar fácilmente nuevos mecanismos de notificación (por ejemplo, enviar correo, registrar logs) sin cambiar `OrderManager`.
    
-   Reduce el acoplamiento entre la lógica de negocio (gestión de pedidos) y las formas de comunicación (**Single Responsibility**).
    
-   Facilita pruebas y extensiones futuras del sistema.
    

----------

## 5. Buenas prácticas de ingeniería de software

El proyecto aplica varias buenas prácticas:

1.  **Modularización y separación de responsabilidades (SRP – Single Responsibility Principle)**
    
    -   Cada archivo tiene una responsabilidad clara (clientes, ítems, decoradores, pedidos, observer, personal, main).
        
    -   Cada clase tiene un propósito bien definido (por ejemplo, `Barista` solo prepara bebidas; `OrderManager` solo gestiona pedidos y notificaciones).
        
2.  **Alta cohesión y bajo acoplamiento**
    
    -   Los decoradores no dependen de detalles internos de `BasicBeverage` o `BasicFood`, solo de la interfaz `MenuItem`.
        
    -   El módulo de notificaciones (`observer.py`) está desacoplado de cómo se representan los pedidos.
        
3.  **Patrón Open/Closed (OCP)**
    
    -   Es posible agregar nuevos extras (`SoyMilk`, `Vanilla`, etc.) implementando nuevos decoradores sin modificar el código existente.
        
    -   Es posible agregar nuevos observadores (por ejemplo, `EmailNotificationService`) sin cambiar `OrderManager`.
        
4.  **Uso de type hints y dataclasses**
    
    -   Se utilizan anotaciones de tipo (`-> None`, `List[Order]`, etc.) para mejorar legibilidad y facilitar herramientas de análisis estático.
        
    -   Se usa `@dataclass` en `Customer` y `Order` para evitar código repetitivo y dejar explícito que son estructuras de datos.
        
5.  **Nombres descriptivos y consistentes**
    
    -   Clases como `BasicBeverage`, `PastryChef`, `NotificationService` describen claramente su función.
        
    -   Métodos como `prepare`, `add_order`, `pending_orders` son autoexplicativos.
        
6.  **Código extendible y fácil de probar**
    
    -   La lógica de negocio está concentrada en clases con métodos simples.
        
    -   La simulación en `main.py` es un “script” muy delgado: se podría reemplazar por una interfaz de usuario o tests automáticos sin reescribir el core.
        