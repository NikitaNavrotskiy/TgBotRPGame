from typing import Optional

import database as db
from .quest import Quest


class NPC:
    """
    This class represents npc.

    :param id: Unique identifier according database.
    :param name: Name of the npc.
    :param description: Description of the npc.
    :param phrase: Personal phrase of the npc.
    :param quests: List of quests of the npc.
    :param image: Filepath to appropriate image of the npc.
    """

    def __init__(self, npc_db: db.NPC, completed_quests: list[int]) -> None:
        """
        Constructor method.
        """        

        self.id: int = npc_db.id
        self.name: str = npc_db.name
        self.description: str = npc_db.description
        self.phrase: str = npc_db.phrase
        self.quests: list[Quest] = [Quest(quest)
                                    for quest in filter(lambda q: q.id not in completed_quests, npc_db.quests)]
        self.image: str = npc_db.image

    def find_quest(self, raw_str: str) -> Optional[Quest]:
        """
        Find corresponding quest from start of the string.

        :param raw_str: String to find in.
        :return: instance of found quest or None otherwise.
        """

        for quest in self.quests:
            if raw_str.startswith(quest.name):
                return quest
        return None
