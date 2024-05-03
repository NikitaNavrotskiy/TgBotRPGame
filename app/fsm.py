from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FSM_Start(StatesGroup):
    """
    Class represents finite state machine's state 
    before the game.

    :param player_name: state when we request user's name.
    """

    player_name = State()


class FSM_Welcome(StatesGroup):
    """
    Class represents finite state machine's state 
    in the begging of the game.

    :param start_game: State when user choose to start the game.
    :param help: State when user choose to display help.
    """

    start_game = State()
    help = State()


class FSM_Location(StatesGroup):
    """
    Class represents finite state machine's state 
    when user on some location.

    :param start: Main state when user seeing description of
        location.
    :param choose_act: State when user choose his
        action on the location.
    :param where_to_go: State when user choose way to relocate.
    """

    start = State()
    choose_act = State()
    where_to_go = State()


class FSM_Conversation(StatesGroup):
    """
    Class represents finite state machine's state 
    when user has conversation with npc.

    :param choose_npc: State when user choose npc to
        talk with.
    :param list_of_quest: State when user choose to see quests
        npc has.
    :param give_message: State when user choose to tranfer message.
    """

    choose_npc = State()
    list_of_quest = State()
    give_message = State()


class FSM_Battle(StatesGroup):
    """
    Class represents finite state machine's state
    when user has battle with enemy.

    :param battle: State when user has battle with
        enemy.
    """

    battle = State()
    congratulation = State()


class FSM_Attack(StatesGroup):
    """
    Class represents finite state machine's state 
    when user during attack action.

    :param choose_enemy: State when user choose enemy to attack.
    :param descr: State when user can see description of the enemy.
    :param process: State that corresponding to battle process.
    """

    choose_enemy = State()
    descr = State()
    process = State()


class FSM_Quest(StatesGroup):
    """
    Class represents finite state machine's state 
    when user Completing quest.

    :param descr: State when user seeing quest's description.
    :param process: State when user completing the quest.
    """

    descr = State()
    process = State()


class FSM_Protagonist_Menu(StatesGroup):
    """
    Class represents finite state machine's state 
    when user viewing protagonist's quests.

    :param process: State when user opens menu
    :param quest_description: State when user viewing
        protagonist's quests.
    :param quest_process: State when user viewing
        chosen quest.
    """

    process = State()
    quest_description = State()
    quest_process = State()


class FSM_End(StatesGroup):
    """
    Class represents finite state machine's state 
    when user has died or completed the game.

    :param completed: State when game is completed.
    :param dead: State when user is dead.
    """

    completed = State()
    dead = State()
