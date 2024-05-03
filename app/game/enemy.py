import random

import database as db


class Enemy:
    """
    This class represents enemy.

    :param id: Unique identifier according database.
    :param name: Name of the enemy.
    :param description: Description of the enemy.
    :param phrase: Personal phrase of the enemy.
    :param level: Level of the enemy.
    :param hp: The amount of healph of the enemy.
    :param damage: the amount of damage from the enemy.
    :param items: List of items that enemy has.
    :param image: Filepath to appropriate image of the enemy.
    """

    def __init__(self, enemy_db: db.Enemy):
        """
        Constructor method. Stores values from db.Enemy instance
        to game class.
        
        :param enemy_db: db.Enemy instance.
        """
        self.id: int = enemy_db.id
        self.name: str = enemy_db.name
        self.description: str = enemy_db.description
        self.phrase: str = enemy_db.phrase
        self.level: int = enemy_db.level
        self.hp: int = enemy_db.health
        self.max_hp: int = enemy_db.health
        self.is_dead: bool = False
        self.damage: int = enemy_db.damage
        self.items: list[str] = [i.name for i in enemy_db.items]
        self.image: str = enemy_db.image

    def roll(self) -> int:
        """
        Method represents throwing a cube with values 1-6
        (all included) + level value.

        :return: appropriate value.
        """

        return random.randint(1, 6) + self.level

    def take_hit(self, value: int = 1) -> bool:
        """
        Method to decrease enemy's healph after protagonist's
        hit.

        :param value: Protagonist's damage.
        :return: Has enemy died.
        """

        self.hp -= value
        if self.hp <= 0:
            self.is_dead = True
            return True
        return False
