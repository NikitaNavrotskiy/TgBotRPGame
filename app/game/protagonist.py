import time
import random
from typing import Optional, Tuple
from sqlalchemy.orm import Session

import database as db
from database import QuestType
from .direction import Direction
from .location import Location
from .enemy import Enemy
from .npc import NPC
from .quest import Quest


PROTAGONIST_HEAL_INTERVAL = 30


class ProtagonistDead(Exception):
    pass


class Protagonist:
    """
    This class represents enemy.

    :param id: Unique identifier according database.
    :param name: Name of the player.
    :param hp: Current health of the player.
    :param level: Current level of the player.
    :param damage: The amount of damage player does.
    :param inventory: Inventory that saves received items.
    :param session: Session of the database.
    :param current_location: Current location where player is located.
    :param current_quests: List of quests whick player has been taken.
    :param completed_quests: List of completed quests by player.
    :param killed_enemies: List of killed enemies by player.
    :param heal_timestamp: Last time of healing the protagonist.
    """

    def __init__(self, name: str, id: int, session: Session):
        """
        Conctructor method.
        """
        self.id: int = id
        self.name: str = name
        self.hp: int = 10
        self.level: int = 1
        self.damage: int = 1
        self.inventory = {}
        self.session: Session = session
        self.current_location: Location = Location(session.query(db.Location)
                                                   .filter(db.Location.id == 1).first(), [], [])
        self.current_quests: list[Quest] = []
        self.completed_quests: list[int] = []
        self.killed_enemies: list[int] = []
        self.heal_timestamp = time.time()

    def roll(self) -> int:
        """
        Method represents throwing a cube with values 1-6
        (all included) + level value.

        :return: appropriate value.
        """

        return random.randint(1, 6) + self.level

    def attack(self, enemy: Enemy) -> Tuple[int, int]:
        """
        Function that represents attack action vs <enemy> enemy.

        :param enemy: Enemy to attack.
        :return: Protagonist's roll and enemy's rool
        """

        enemy_roll = enemy.roll()
        protagonist_roll = self.roll()

        if enemy_roll < protagonist_roll:
            if enemy.take_hit(self.damage):
                for item in enemy.items:
                    self.take(item)
                self.killed_enemies.append(enemy.id)
        elif enemy_roll > protagonist_roll:
            self.take_hit(enemy.damage)

        return protagonist_roll, enemy_roll

    def take_hit(self, value: int = 1) -> None:
        """
        Function to take a hit from some enemy with <value> damage.

        :param value: Amount of damage. 
        """

        self.hp -= value
        if self.hp <= 0:
            raise ProtagonistDead("You died")

    def heal(self) -> None:
        """
        Function to heal protagonist if enough time has passed.
        """

        new_timestamp: float = time.time()
        heal_hours: int = int((new_timestamp - self.heal_timestamp) // PROTAGONIST_HEAL_INTERVAL)
        if heal_hours != 0:
            self.heal_timestamp = new_timestamp
            self.hp = min(self.hp + heal_hours * self.level, 10 * self.level)

    def health(self) -> int:
        """
        Calles heal() method to renew info and 
        returns current value of protagonist's health
        """

        self.heal()
        return self.hp

    def advance_level(self, value: int = 1) -> None:
        """
        Increases the level and dependend 
        damage and hp values.

        :param value: Times to increase level.
        """
        self.level += value
        self.damage += value
        self.hp = 10 * self.level

    def go(self, direction: Direction) -> None:
        """
        Relocate player to another Location by the <direction>
        direction.

        :param direction: Direction to go.
        """
        if direction.location_level > self.level:
            return
        self.current_location = Location(self.session.query(db.Location)
                                         .filter(db.Location.id == direction.location_id).first(),
                                         self.killed_enemies,
                                         self.completed_quests)

    def whereami(self) -> Location:
        """
        Returns current location.

        :return: Current location.
        """

        return self.current_location

    def new_locations(self) -> list[str]:
        """
        Returns list of locations.

        :return: Current location.
        """

        result: list[str] = []
        for loc in self.session.query(db.Location).filter(db.Location.level == self.level).all():
            result.append(loc.name)
        return result

    def take(self, item: str) -> None:
        """
        Take an item to the inventory.

        :param item: Item to take.
        """

        self.inventory[item] = self.inventory.get(item, 0) + 1

    def give(self, item: str) -> None:
        """
        Give the <item> Item.

        :param item: Item to give.
        """

        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]

    def complete_quest(self, quest: Quest) -> None:
        """
        Completing the <quest> quest.

        :param quest: Quest needed to be completed.
        """

        if quest.quest_type == QuestType.Bring:
            self.give(quest.goal)
        self.completed_quests.append(quest.id)
        self.current_quests.remove(quest)
        self.advance_level()

    def get_killed_enemies(self) -> list[str]:
        """
        Generates list of enemy names killed by protagonist.

        :return: list of enemy names.
        """
        enemies = []
        for enemy_id in self.killed_enemies:
            enemy = self.session.query(db.Enemy).filter(db.Enemy.id == enemy_id).first()
            if enemy:
                enemies.append(enemy.name)
        return enemies

    def take_quest(self, quest: Quest) -> None:
        """
        Take the quest action.

        :param quest: Quest to take.
        """

        self.current_quests.append(quest)

    def has_quest(self, quest: Quest) -> bool:
        """
        Checks if quest has been taken.

        :return: True if taken, False otherwise.
        """

        for q in self.current_quests:
            if q.id == quest.id:
                return True
        return False

    def can_complete(self, quest: Quest) -> bool:
        """
        Checks if quest can be completed right now.
        Works only with Bring and Kill quests

        :return: True if yes, False otherwise.
        """

        if self.has_quest(quest):
            if quest.quest_type == QuestType.Bring and self.inventory.get(quest.goal):
                return True
            if quest.quest_type == QuestType.Kill and quest.goal in self.killed_enemies:
                return True
        return False

    def npc_has_not_taken_quests(self, npc: NPC):
        """
        Checks if npc has quest not taken by protagonist.

        :param npc: NPC to check quests.
        :return: True if there is not taken quest, False otherwise.
        """
        for quest in npc.quests:
            if not self.has_quest(quest):
                return True
        return False

    def npc_has_quests_to_complete(self, npc: NPC):
        """
        Checks if npc has quest not taken by protagonist.

        :param npc: NPC to check quests.
        :return: True if there is not taken quest, False otherwise.
        """
        for quest in npc.quests:
            if self.can_complete(quest):
                return True
        return False

    def messages_for(self, npc: NPC) -> list[str]:
        """
        Find npcs for whom the message is sent.

        :param npc: Npc for the search.
        :return: List of npcs names.
        """

        givers = []
        for quest in self.current_quests:
            if quest.quest_type == QuestType.Talk and quest.goal == npc.id:
                givers.append(quest.npc_name)
        return givers

    def find_quest(self, raw_str: str) -> Optional[Quest]:
        """
        Find corresponding quest from start of the string.

        :param raw_str: String to find in.
        :return: instance of found quest or None otherwise.
        """

        for quest in self.current_quests:
            if raw_str.startswith(quest.name):
                return quest
        return None

    def find_messager(self, raw_str: str) -> Optional[Quest]:
        """
        Find corresponding quest by npc_name from end of the string.

        :param raw_str: String to find in.
        :return: instance of found quest or None otherwise.
        """

        for quest in self.current_quests:
            if raw_str.endswith(quest.npc_name):
                return quest
        return None
