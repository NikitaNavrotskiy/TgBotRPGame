from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from game import Direction, Enemy, NPC, Protagonist, QuestType, Quest


def make_keyboard_welcome() -> ReplyKeyboardMarkup:
    """
    Funciton generates starting keyboard.

    :return: Appropriate keyboard
    """

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Начать игру')]
    ], resize_keyboard=True)
    

def make_keyboard_location_start() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with 
    possible actions on the location.

    :return: Appropriate keyboard
    """

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Поговорить'), KeyboardButton(text='Осмотреть врага')],
        [KeyboardButton(text='Отправиться'), KeyboardButton(text='Меню героя')],
    ], resize_keyboard=True)


def make_keyboard_congratulation() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard when
    quest has been done or an enemy has been defeated.

    :return: Appropriate keyboard
    """

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отлично')]
    ], resize_keyboard=True)


def make_keyboard_enemy_description() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with 
    possible actions with enemies.

    :return: Appropriate keyboard
    """

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Напасть'), KeyboardButton(text='Назад')],
    ], resize_keyboard=True)


def make_keyboard_battle() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with
    possible actions with enemies.

    :return: Appropriate keyboard
    """

    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Атаковать'), KeyboardButton(text='Сбежать')],
    ], resize_keyboard=True)


def make_keyboard_talk(npcs: List[NPC]) -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with npcs
    user can have conversation.

    :param npcs: List of npcs
    :return: Appropriate keyboard
    """
    
    buttons: List[List[KeyboardButton]] = []

    for npc in npcs:
        buttons.append([KeyboardButton(
            text='Поговорить с {name}'.format(
                name=npc.name
        )
    )])
    buttons.append([KeyboardButton(
        text='Отмена'
    )])
        
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def make_keyboard_talk_actions(prota: Protagonist, npc: NPC) -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with
    possible actions with given npc.

    :param prota: Instance of Protagonist.
    :param npc: Current npc.
    :return: Appropriate keyboard.
    """

    buttons: List[List[KeyboardButton]] = [[KeyboardButton(text='Список заданий')]]
    for npc_name in prota.messages_for(npc):
        buttons.append([KeyboardButton(text=f'Передать сообщение от {npc_name}')])
    buttons.append([KeyboardButton(text='Назад')])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def make_keyboard_proto_quest_list(prota: Protagonist, quests: List[Quest],
                                   talk_state: bool = False):
    """
    Funciton generates keyboard with
    given list of quests.

    :param prota: Instance of Protagonist.
    :param quests: List of quests.
    :param talk_state: Flag to print 'taken' part
    :param npc: NPC if talk_state is True
    :return: Appropriate keyboard.
    """
    
    buttons: List[List[KeyboardButton]] = []

    for quest in quests:
        text = f'    {quest.name}'
        match quest.quest_type:
            case QuestType.Kill:
                text += ' ⚔️'
            case QuestType.Bring:
                text += ' 💍'
            case QuestType.Talk:
                text += ' 💬'

        if talk_state and prota.has_quest(quest):
            if prota.can_complete(quest):
                text += ' (можно сдать)'
            else:
                text += ' (взято)'
        buttons.append([KeyboardButton(text=text)])

    buttons.append([KeyboardButton(text='Отмена')])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)  


def make_keyboard_quests_list(proto: Protagonist, npc: NPC) -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with
    list of quests of npc.

    :param proto: Instance of Protagonist
    :param npc: Current npc.
    :return: Appropriate keyboard.
    """

    return make_keyboard_proto_quest_list(proto, npc.quests, talk_state=True)


def make_keyboard_quest_acts(proto: Protagonist, quest: Quest):
    """
    Funciton generates keyboard with
    actions for quest (Taken or not).

    :param proto: Instance of Protagonist.
    :param quest: Chosen quest.
    :return: Appropriate keyboard.
    """

    if proto.has_quest(quest):
        complete_button_text = None
        if quest.quest_type == QuestType.Kill and quest.goal in proto.killed_enemies:
            complete_button_text = 'Отчитаться об убийстве'
        elif quest.quest_type == QuestType.Bring and quest.goal in proto.inventory:
            complete_button_text = 'Отдать предмет'
        if complete_button_text:
            return ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text=complete_button_text)],
                [KeyboardButton(text='Назад')]
            ], resize_keyboard=True)
        return ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Назад')]
        ], resize_keyboard=True)
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Взять Задание'), KeyboardButton(text='Назад')]
    ], resize_keyboard=True)


def make_keyboard_attack_list(enemies: List[Enemy]) -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with
    enemies on the current location user
    can attack.

    :param enemies: List of enemies.
    :return: Appropriate keyboard.
    """

    buttons: List[List[KeyboardButton]] = []

    for enemy in enemies:
        text = f'{enemy.name}\n'
        buttons.append([KeyboardButton(text=text)])
    buttons.append([KeyboardButton(text='Отмена')])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def make_keyboard_directions_list(directions: List[Direction], prota: Protagonist) -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with
    possible directions to relocate.

    :param directions: List of directions.
    :param prota: Protagonist.
    :return: Appropriate keyboard.
    """

    buttons: List[List[KeyboardButton]] = []

    for direction in directions:
        text = f'{direction.name}'
        if direction.location_level > prota.level:
            text += f' (закрыто, {direction.location_level} ур.)'
        buttons.append([KeyboardButton(text=text + '\n')])
    buttons.append([KeyboardButton(text='Отмена')])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def make_keyboard_quest_description_back() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with one button: Back.

    :return: Appropriate keyboard.
    """

    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]], resize_keyboard=True)


def make_keyboard_protagonist_menu() -> ReplyKeyboardMarkup:
    """
    Funciton generates keyboard with one button: Back.

    :return: Appropriate keyboard.
    """

    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Профиль героя'), KeyboardButton(text='Список заданий')],
                                         [KeyboardButton(text='Назад')]], resize_keyboard=True)
