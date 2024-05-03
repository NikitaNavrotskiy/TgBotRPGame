from typing import Optional

import database as db
from .direction import Direction
from .enemy import Enemy
from .npc import NPC


class Location:
    """
    Class represents game's location.

    :param id: Unique identifier according database.
    :param name: Name of the location.
    :param level: Level that protagonist should reach to unlock
        this location.
    :param description: Description of the location.
    :param npc: List of npcs on the location.
    :param enemies: List of enemies on the location.
    :param image: Filepath to appropriate image of the location.
    """
    def __init__(self, location_db: db.Location | None, killed_enemies: list[int], completed_quests: list[int]):
        """
        Constructor method.
        """

        if not location_db:
            raise RuntimeError("Non existing location in database")
        self.id: int = location_db.id
        self.name: str = location_db.name
        self.level: int = location_db.level
        self.description: str = location_db.description
        self.directions: list[Direction] = [Direction(*d) for d in location_db.directions()]
        self.npc: list[NPC] = [NPC(n, completed_quests) for n in location_db.npc]
        self.enemies: list[Enemy] = [Enemy(e)
                                     for e in filter(lambda e: e.id not in killed_enemies, location_db.enemies)]
        self.image: str = location_db.image

    def find_npc(self, raw_str: str) -> Optional[NPC]:
        """
        Find corresponding npc from end of the string.

        :param raw_str: String to find in.
        :return: instance of found npc or None otherwise.
        """

        for npc in self.npc:
            if raw_str.endswith(npc.name):
                return npc
        
        return None
