import database as db
from database import QuestType


class Quest:
    """
    This class represents quest.

    :param id: Unique identifier according database.
    :param name: Name of the quest.
    :param description: Description of the quest.
    :param congratulation: Message after passing the quest.
    :param npc_name: Name of npc who owns it.
    :param quest_type: Type of quest: Bring something,
        Kill someone or Talk to someone.
    :param goal: Goal to pass the quest.
    """

    def __init__(self, quest_db: db.Quest):
        """
        Constructor method.
        """

        self.id: int = quest_db.id
        self.name: str = quest_db.name
        self.description: str = quest_db.description
        self.congratulation: str = quest_db.congratulation
        self.is_final: bool = quest_db.is_final
        self.npc_name: str = quest_db.npc.name
        self.quest_type: QuestType = quest_db.type()

        if self.quest_type == QuestType.Kill:
            self.goal: str | int = quest_db.goal_enemy_id
        elif self.quest_type == QuestType.Bring:
            self.goal: str | int = quest_db.goal_item.name
        else:
            self.goal: str | int = quest_db.goal_npc_id

    def __eq__(self, value: object) -> bool:
        """
        Overloading of == method.
        """
        
        return self.id == value.id
