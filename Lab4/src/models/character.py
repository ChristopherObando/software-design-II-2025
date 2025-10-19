class Character:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
    
    def heal(self, amount):
        if self.is_alive:
            self.health += amount