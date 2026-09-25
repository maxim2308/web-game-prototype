"""
Player class for web game
Tested in E2B sandbox - ALL TESTS PASSED
"""

from typing import Dict


class Player:
    """Игрок с системой опыта, уровней и инвентаря"""
    
    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.inventory: Dict[str, int] = {}
    
    def add_xp(self, amount: int) -> bool:
        """Добавить опыт. Возвращает True если получен уровень"""
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.5)
            leveled = True
        return leveled
    
    def add_item(self, item: str, quantity: int = 1):
        """Добавить предмет в инвентарь"""
        self.inventory[item] = self.inventory.get(item, 0) + quantity
    
    def remove_item(self, item: str, quantity: int = 1) -> bool:
        """Удалить предмет. Возвращает False если недостаточно"""
        if self.inventory.get(item, 0) < quantity:
            return False
        self.inventory[item] -= quantity
        if self.inventory[item] == 0:
            del self.inventory[item]
        return True
    
    def to_dict(self) -> dict:
        """Сериализация для сохранения"""
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "inventory": self.inventory
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Десериализация из сохранения"""
        player = cls(data["name"])
        player.level = data["level"]
        player.xp = data["xp"]
        player.xp_to_next = data["xp_to_next"]
        player.inventory = data["inventory"]
        return player


# Тесты (выполнены в E2B sandbox)
if __name__ == "__main__":
    # Создаём игрока
    hero = Player("Hero")
    
    # Тест 1: Добавление опыта
    assert hero.level == 1
    hero.add_xp(50)
    assert hero.level == 1
    assert hero.xp == 50
    
    # Тест 2: Level up
    leveled = hero.add_xp(100)
    assert leveled == True
    assert hero.level == 2
    
    # Тест 3: Инвентарь
    hero.add_item("potion", 2)
    assert hero.inventory["potion"] == 2
    
    # Тест 4: Удаление предметов
    assert hero.remove_item("potion", 1) == True
    assert hero.inventory["potion"] == 1
    
    # Тест 5: Сериализация
    data = hero.to_dict()
    hero2 = Player.from_dict(data)
    assert hero2.name == hero.name
    assert hero2.level == hero.level
    
    print("ALL TESTS PASSED")
    print(hero.to_dict())
