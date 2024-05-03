from enum import Enum
from typing import List, Optional, Tuple

from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class QuestType(Enum):
    """
    Enumeration represents types of quests: `Bring`, `Kill`, `Talk`.
    """

    Bring = 'Bring'
    Kill = 'Kill'
    Talk = 'Talk'


class Base(DeclarativeBase):
    """
    Base class.
    """

    pass


class Location(Base):
    """
    Class represents Location object in database.

    :param id: id in database.
    :param image: filepath of location image.
    :param name: name of location.
    :param description: description of location.
    :param level: minimal level of protagonist to enter location.
    :param npc: list of NPC on this location.
    :param enemies: list of Enemies on this location.
    :param from_directions: list of directions from this location to others
    """

    __tablename__ = 'location'
    __table_args__ = (
        UniqueConstraint('name'),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(256), nullable=True)

    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(200))
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    npc: Mapped[List['NPC']] = relationship(back_populates='location')
    enemies: Mapped[List['Enemy']] = relationship(back_populates='location')

    def __init__(self, name: str, description: str, level: int, id: int = None, image: str = '') -> None:
        """Constructor method
        """
        super().__init__()
        if id:
            self.id = id
        self.image = image
        self.name = name
        self.description = description
        self.level = level

    def directions(self) -> List[Tuple[str, int, int]]:
        """
        Method to get all directions from the location.

        :return: List[Tuple[{direction name}, {location id}, {location_level}]] for location
        where direction lead to.
        """

        return [(d.name, d.to_location.id, d.to_location.level) for d in self.from_directions]


class Direction(Base):
    """
    Class represents Direction object in database.

    :param id: id in database.
    :param name: name of direction.
    :param from_location_id: id of location in the starting point.
    :param to_location_id: id of location in the ending point.
    """
    __tablename__ = 'direction'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40))
    from_location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    to_location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    from_location = relationship(
        Location, primaryjoin=from_location_id == Location.id, backref="from_directions"
    )
    to_location = relationship(
        Location, primaryjoin=to_location_id == Location.id, backref="to_directions"
    )

    def __init__(self, name: str, from_location: Location = None, to_location: Location = None,
                 id: int = None, from_location_id: int = None, to_location_id: int = None):
        """Constructor method
        """

        super().__init__()
        if id:
            self.id = id
        self.name = name
        if from_location:
            self.from_location = from_location
        if to_location:
            self.to_location = to_location
        self.from_location_id = from_location_id
        self.to_location_id = to_location_id


class NPC(Base):
    """
    Class represents NPC object in database.

    :param id: id in database.
    :param image: filepath of NPC image.
    :param name: name of NPC.
    :param description: description of NPC.
    :param phrase: phrase of NPC.
    :param location: location of NPC.
    :param quests: list of Quests given by this NPC.
    """
    __tablename__ = 'npc'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    image: Mapped[str] = mapped_column(String(256), nullable=True)

    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(100))
    phrase: Mapped[str] = mapped_column(String(200))
    location: Mapped['Location'] = relationship(back_populates='npc')
    quests: Mapped[List['Quest']] = relationship(back_populates='npc', foreign_keys='[Quest.npc_id]')

    def __init__(self, name: str, description: str, phrase: str,
                 location: Location = None, id: int = None, image: str = '', location_id: int = None) -> None:
        """Constructor method
        """
        super().__init__()
        if id:
            self.id = id
        self.image = image
        self.name = name
        self.description = description
        self.phrase = phrase
        if location:
            self.location = location
        if location_id:
            self.location_id = location_id


class Enemy(Base):
    """
    Class represents Enemy object in database.

    :param id: id in database.
    :param image: filepath of Enemy image.
    :param name: name of Enemy.
    :param description: description of Enemy.
    :param phrase: phrase of Enemy.
    :param location: location of Enemy.
    :param level: Enemy level.
    :param health: Enemy health.
    :param damage: Enemy damage.
    :param items: list of Items dropped by this Enemy.
    """
    __tablename__ = 'enemy'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    image: Mapped[str] = mapped_column(String(256), nullable=True)
    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(100))
    phrase: Mapped[str] = mapped_column(String(200))
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    health: Mapped[int] = mapped_column(Integer, nullable=False)
    damage: Mapped[int] = mapped_column(Integer, nullable=False)
    items: Mapped[List['Item']] = relationship(back_populates='enemy')
    location: Mapped['Location'] = relationship(back_populates='enemies')

    def __init__(self, name: str, description: str, phrase: str, level: int, health: int, damage: int,
                 location: Location = None, id: int = None, image: str = '', location_id: int = None) -> None:
        """Constructor method
        """
        super().__init__()
        if id:
            self.id = id
        self.image = image
        self.name = name
        self.description = description
        self.phrase = phrase
        self.level = level
        self.health = health
        self.damage = damage
        if location:
            self.location = location
        if location_id:
            self.location_id = location_id


class Item(Base):
    """
    Class represents Item object in database.

    :param id: id in database.
    :param name: name of Item.
    :param enemy_id: id of Enemy that drops this item.
    :param enemy: Enemy that drops this item.
    """
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enemy_id: Mapped[int] = mapped_column(ForeignKey('enemy.id'))
    name: Mapped[str] = mapped_column(String(40))
    enemy: Mapped['Enemy'] = relationship(back_populates='items')

    def __init__(self, name: str, enemy: Enemy = None, id: int = None, enemy_id: int = None) -> None:
        """Constructor method
        """
        super().__init__()
        if id:
            self.id = id
        self.name = name
        if enemy:
            self.enemy = enemy
        if enemy_id:
            self.enemy_id = enemy_id


class Quest(Base):
    """
    Class represents Quest object in database.

    :param id: id in database.
    :param npc_id: id of NPC that gives this quest.
    :param name: name of Quest.
    :param description: Quest description.
    :param congratulation: Quest congratulation.
    :param npc: NPC that gives this quest.
    :param goal_item_id: id of Item to bring if QuestType is Bring.
    :param goal_item: Item to bring if QuestType is Bring.
    :param goal_npc_id: id of NPC to talk if QuestType is Talk.
    :param goal_enemy_id: id of Enemy to kill if QuestType is Kill.
    """
    __tablename__ = 'quest'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    npc_id: Mapped[int] = mapped_column(ForeignKey('npc.id'))

    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(200))
    congratulation: Mapped[str] = mapped_column(String(200))
    is_final: Mapped[bool] = mapped_column(Boolean)
    npc: Mapped['NPC'] = relationship(back_populates='quests', foreign_keys=[npc_id])

    goal_item_id: Mapped[Optional[int]] = mapped_column(ForeignKey('item.id'))
    goal_npc_id: Mapped[Optional[int]] = mapped_column(ForeignKey('npc.id'))
    goal_enemy_id: Mapped[Optional[int]] = mapped_column(ForeignKey('enemy.id'))
    goal_item: Mapped['Item'] = relationship(foreign_keys=[goal_item_id])

    def __init__(self, name: str, description: str, congratulation: str,
                 goal: int, goal_type: QuestType, npc: NPC = None, id: int = None, npc_id: int = None,
                 is_final: bool = False) -> None:
        """Constructor method
        """
        super().__init__()
        if id:
            self.id = id
        self.name = name
        self.description = description
        self.congratulation = congratulation
        self.is_final = is_final
        if npc:
            self.npc = npc
        if npc_id:
            self.npc_id = npc_id
        if goal_type == QuestType.Bring:
            self.goal_item_id = goal
        elif goal_type == QuestType.Talk:
            self.goal_npc_id = goal
        elif goal_type == QuestType.Kill:
            self.goal_enemy_id = goal

    def __str__(self) -> str:
        """
        Method to get string representation of Object.

        :return: str.
        """

        return self.name
    
    def type(self) -> QuestType:
        """
        Method to get type of the quest.

        :return: QuestType.
        """

        if self.goal_item_id:
            return QuestType.Bring
        if self.goal_npc_id:
            return QuestType.Talk
        if self.goal_enemy_id:
            return QuestType.Kill
        raise RuntimeError('Quest has no goal')
