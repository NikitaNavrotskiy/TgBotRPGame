import json
import sys
from database import *


DATA_FILE = 'default_db.json'


def load_location(session: Session, location: dict) -> None:
    """
    Loading all locations from json to the database.

    :param session: Session of the database.
    :param location: Dictionary that contains info
        about location.
    """

    session.add(Location(location['name'],
                         location['description'],
                         location['level'],
                         id=location['id'],
                         image=location.get('image')))


def load_direction(session: Session, direction: dict) -> None:
    """
    Loading all directions from json to the database.

    :param session: Session of the database.
    :param direction: Dictionary that contains info
        about direction.
    """

    session.add(Direction(direction['name'],
                          id=direction['id'],
                          from_location_id=direction['from_location_id'],
                          to_location_id=direction['to_location_id']))


def load_npc(session: Session, npc: dict) -> None:
    """
    Loading all npcs from json to the database.

    :param session: Session of the database.
    :param npc: Dictionary that contains info
        about npc.
    """

    session.add(NPC(npc['name'],
                    npc['description'],
                    npc['phrase'],
                    id=npc['id'],
                    image=npc.get('image'),
                    location_id=npc['location_id']))


def load_enemy(session: Session, enemy: dict) -> None:
    """
    Loading all enemies from json to the database.

    :param session: Session of the database.
    :param enemy: Dictionary that contains info
        about enemy.
    """

    session.add(Enemy(enemy['name'],
                      enemy['description'],
                      enemy['phrase'],
                      enemy['level'],
                      enemy['health'],
                      enemy['damage'],
                      id=enemy['id'],
                      image=enemy.get('image'),
                      location_id=enemy['location_id']))


def load_item(session: Session, item: dict) -> None:
    """
    Loading all items from json to the database.

    :param session: Session of the database.
    :param item: Dictionary that contains info
        about items.
    """

    session.add(Item(item['name'],
                     id=item['id'],
                     enemy_id=item['enemy_id']))


def load_quest(session: Session, quest: dict) -> None:
    """
    Loading all quests from json to the database.

    :param session: Session of the database.
    :param quest: Dictionary that contains info
        about quest.
    """
    
    quest_type: QuestType = QuestType.Kill
    goal: int = quest.get('goal_enemy_id')
    if quest.get('goal_item_id'):
        quest_type = QuestType.Bring
        goal = quest.get('goal_item_id')
    elif quest.get('goal_npc_id'):
        quest_type = QuestType.Talk
        goal = quest.get('goal_npc_id')
    session.add(Quest(quest['name'],
                      quest['description'],
                      quest['congratulation'],
                      goal,
                      quest_type,
                      id=quest['id'],
                      npc_id=quest['npc_id'],
                      is_final=quest.get('is_final', False)))


def main() -> int:
    """
    Entry point for load_all.py
    """

    with open(DATA_FILE, 'r', encoding='utf-8') as fp, Session() as session:
        data: dict = json.load(fp)
        for location in data['locations']:
            load_location(session, location)
        for direction in data['directions']:
            load_direction(session, direction)
        for npc in data['npc']:
            load_npc(session, npc)
        for enemy in data['enemies']:
            load_enemy(session, enemy)
        for item in data['items']:
            load_item(session, item)
        session.commit()
        for quest in data['quests']:
            load_quest(session, quest)
        session.commit()
    return 0


if __name__ == '__main__':
    sys.exit(main())
