from customers import Customer
from menu_items import BasicBeverage, BasicFood
from decorators import Milk, Cinnamon, Cream, ChocolateFilling
from orders import Order, OrderManager
from staff import Barista, PastryChef
from observer import NotificationService


def build_sample_orders(order_manager: OrderManager) -> None:
    """Construye los pedidos del ejemplo dado en el enunciado."""
    # Cliente Ana
    ana = Customer("Ana")
    print(f"Cliente: {ana.name}")

    coffee = BasicBeverage("Cafe", 1200.0)
    coffee = Milk(coffee)
    coffee = Cinnamon(coffee)
    print(f"Ordena un {coffee.description().lower()}")

    croissant = BasicFood("Croissant", 1500.0)
    croissant = ChocolateFilling(croissant)
    print(f"Ordena un {croissant.description().lower()}")

    order_manager.add_order(Order(ana, coffee))
    order_manager.add_order(Order(ana, croissant))

    # Cliente Carlos
    carlos = Customer("Carlos")
    print(f"Cliente: {carlos.name}")

    green_tea = BasicBeverage("Te verde", 1000.0)
    print(f"Ordena un {green_tea.description().lower()}")

    double_espresso = BasicBeverage("Cafe doble espresso", 1300.0)
    double_espresso = Cream(double_espresso)
    print(f"Ordena un {double_espresso.description().lower()}")

    order_manager.add_order(Order(carlos, green_tea))
    order_manager.add_order(Order(carlos, double_espresso))


def main() -> None:
    print("=== Simulacion de Cafeteria ===")

    # Subject en el patrón Observer
    order_manager = OrderManager()

    # Observador concreto que reacciona cuando se han procesado todos los pedidos
    notification_service = NotificationService()
    order_manager.attach(notification_service)

    # Construimos los pedidos del ejemplo
    build_sample_orders(order_manager)

    # Personal que prepara los pedidos
    barista = Barista()
    pastry_chef = PastryChef()

    # Procesamos todos los pedidos pendientes
    for order in order_manager.pending_orders:
        if order.item.category() == "bebida":
            barista.prepare(order)
        else:
            pastry_chef.prepare(order)

    # Notificamos a los observadores que todos los pedidos están listos
    order_manager.notify("Se notifican los clientes cuando sus pedidos estan listos.")


if __name__ == "__main__":
    main()
