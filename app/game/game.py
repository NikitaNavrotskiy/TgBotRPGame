from typing import Dict, Optional
from aiogram.types import Message

from .direction import Direction
from .enemy import Enemy
from .location import Location
from .protagonist import Protagonist


"""
Dictionary, that saves all sessions through protagonist
instances by tg_tokens. 
"""
protagonists: Dict[int, Protagonist] = {}


def protagonist_add(tg_id: int, protagonist: Protagonist) -> None:
    """
    Adds new user to the <protagonists> dictionary.

    :param tg_id: Telegram id of current user.
    :param protagonist: Protagonist instance.
    """
    protagonists[tg_id] = protagonist


def get_proto_from_msg(message: Message) -> Protagonist:
    """
    Gets protagonist from message, that
    aiogram handler receives from user.

    :param message: Aiogram message instance.
    :return: Instance of Protagonist for current user.
    """

    tg_id = message.from_user.id
    return protagonists[tg_id]


def get_direction_from_msg(prota: Protagonist, raw_msg: str) -> Optional[Direction]:
    """
    Gets direction from message.

    :param prota: instance of Protagonist for current user.
    :return: Appropriate direction.
    """
    
    for direction in prota.whereami().directions:
        if raw_msg == direction.name:
            return direction
        
    return None


def get_enemy_from_msg(location: Location, raw_msg: str) -> Optional[Enemy]:
    """
    Gets enemy from messaage.

    :param location: Current location.
    :param raw_msg: text received from user.
    :return: Appropriate enemy.
    """

    for enemy in location.enemies:
        if enemy.name == raw_msg:
            return enemy
    
    return None
