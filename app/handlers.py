import asyncio
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove

from database import Session
from fsm import *
from game import *
import keyboards as kb
import templates as tp

router = Router()


@router.message(CommandStart())
async def handler_start(message: Message, state: FSMContext) -> None:
    """
    #/START

    '/start' Command handler.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    await state.set_state(FSM_Start.player_name)
    await message.answer('Введите имя игрока: ')


@router.message(FSM_Start.player_name)
async def handler_start_name(message: Message, state: FSMContext) -> None:
    """
    #/START -> WELCOME

    Calls after user entered his name.
    This func renews protagonist for user.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    await state.update_data(player_name=message.text, semaphore=asyncio.Semaphore(1))
    tg_id = message.from_user.id
    cur_proto = Protagonist(message.text, tg_id, Session())
    protagonist_add(tg_id, cur_proto)

    await message.answer(
        tp.template_welcome(cur_proto), 
        reply_markup=kb.make_keyboard_welcome(), parse_mode='HTML'
    )
    await state.set_state(FSM_Welcome.start_game)


@router.message(FSM_Welcome.start_game, F.text == 'Начать игру')
async def handler_welcome_start_game(message: Message, state: FSMContext) -> None:
    """
    #WELCOME -> LOCATION

    Calls after the beginnign of the game. This func
    sends user to the starting location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await state.set_state(FSM_Location.start)
    await handler_location_start(message, state)


async def send_photo_or_text(message: Message, image: str, text: str, keyboard: ReplyKeyboardMarkup) -> None:
    """
    Sends photo if exists, message and keyboard.

    :param message: Message from user.
    :param image: Path to the image.
    :param text: Answer for the user.
    :param keyboard: Keyboard instance attached to the answer.
    """
    
    if image:
        await message.answer_photo(FSInputFile(image), text, reply_markup=keyboard, parse_mode='HTML')
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode='HTML')


@router.message(FSM_Location.start)
async def handler_location_start(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls whenever user goes to the location and
    in the begging of the game. This func
    prints info about current location: name, description,
    character and enemies.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    cur_proto = get_proto_from_msg(message)
    text = tp.location_info(
        cur_proto.current_location.name,
        cur_proto.current_location.description,
        cur_proto.current_location.npc,
        cur_proto.current_location.enemies,
        cur_proto
    )
    await send_photo_or_text(message, cur_proto.current_location.image, text, kb.make_keyboard_location_start())
    await state.set_state(FSM_Location.choose_act)


# Поговрить

@router.message(FSM_Location.choose_act, F.text == 'Поговорить')
async def handler_talk(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls when user wants to talk with npc. Func prints
    list of npcs on the current location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_location = cur_proto.current_location
    if not cur_location.npc:
        await message.answer(tp.no_npc())
        return
    await message.answer(
        tp.talk_with(),
        reply_markup=kb.make_keyboard_talk(cur_location.npc),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Conversation.choose_npc)


@router.message(FSM_Conversation.choose_npc, F.text == 'Отмена')
async def handler_talk_choose_npc_cancel(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls when user doesn't want to talk with current npc. Func prints
    list of npcs on the current location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await handler_location_start(message, state)


@router.message(FSM_Conversation.choose_npc)
async def handler_talk_choose_npc(message: Message, state: FSMContext) -> None:
    """
    #LOCATION -> CONVERSATION

    Calls when user has chosen npc to talk. Displays list
    of action with this npc.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_location = cur_proto.current_location
    cur_npc = cur_location.find_npc(message.text)
    if cur_npc:
        await state.update_data({'cur_npc': cur_npc})
        await handler_talk_choose_npc_main(message, state)


async def handler_talk_choose_npc_main(message: Message, state: FSMContext) -> None:
    """
    Calls after handler_talk_choose_npc() or handler_quest_descr_cancel()
    Displays conversation actions.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    cur_proto = get_proto_from_msg(message)
    data = await state.get_data()
    cur_npc = data['cur_npc']
    await send_photo_or_text(message, cur_npc.image,
                             tp.talk_with_npc(cur_npc),
                             kb.make_keyboard_talk_actions(cur_proto, cur_npc))
    await state.set_state(FSM_Conversation.list_of_quest)


@router.message(FSM_Conversation.list_of_quest, F.text == 'Назад')
async def handler_talk_list_quests_cancel(message: Message, state: FSMContext) -> None:
    """
    #CONVERSATION -> LOCATION

    Calls when user want to go back to location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    await handler_location_start(message, state)


@router.message(FSM_Conversation.list_of_quest, F.text.startswith('Передать сообщение от '))
async def handler_talk_pass_message(message: Message, state: FSMContext) -> None:
    """
    #CONVERSATION -> QUEST_TALK_CONGRATULATION

    Calls after user has chosen npc to talk. Displays
    npc's name, description and phrase. Also list of
    buttons to choose quest or go back.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    data = await state.get_data()
    cur_proto = get_proto_from_msg(message)
    cur_quest = cur_proto.find_messager(message.text)
    cur_npc = data['cur_npc']
    if cur_quest.goal == cur_npc.id:
        cur_proto.complete_quest(cur_quest)
        await message.answer(
            tp.npc_quest_done(cur_proto, cur_quest),
            reply_markup=kb.make_keyboard_talk_actions(cur_proto, cur_npc),
            parse_mode='HTML'
        )


@router.message(FSM_Conversation.list_of_quest)
async def handler_talk_list_quests(message: Message, state: FSMContext) -> None:
    """
    #LIST_OF_QUESTS_NPC -> QUEST_DESCRIPTION_NPC

    Calls after user has chosen npc to talk. Displays
    npc's name, description and phrase. Also list of
    buttons to choose quest or go back.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    cur_proto = get_proto_from_msg(message)
    data = await state.get_data()
    cur_npc = data['cur_npc']
    await message.answer(
        tp.talk_npc_actions(),
        reply_markup=kb.make_keyboard_quests_list(cur_proto, cur_npc),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Quest.descr)


@router.message(FSM_Quest.descr, F.text == 'Отмена')
async def handler_quest_descr_cancel(message: Message, state: FSMContext) -> None:
    """
     #LIST_OF_QUESTS_NPC -> CONVERSATION

    Go back after receiving list of quest by user.
    Sends user to the choice of actions.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    await handler_talk_choose_npc_main(message, state)


@router.message(FSM_Quest.descr)
async def handler_quest_descr(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DESCRIPTION_NPC

    Calls after user has chosen quest of npc. Displays 
    info about quest and buttons: Take quest or Go back.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    data = await state.get_data()
    cur_npc = data['cur_npc']
    cur_proto = get_proto_from_msg(message)
    cur_quest = cur_npc.find_quest(message.text)
    if cur_quest:
        await message.answer(
            tp.npc_quest(cur_quest),
            reply_markup=kb.make_keyboard_quest_acts(cur_proto, cur_quest),
            parse_mode='HTML'
        )
        await state.set_state(FSM_Quest.process)
        await state.update_data({'cur_quest': cur_quest, 'cur_npc': cur_npc})


@router.message(FSM_Quest.process, F.text == 'Взять Задание')
async def handler_quest_take(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DESCRIPTION_NPC -> LIST_OF_QUESTS_NPC

    Calls after user has taken the quest. This quest 
    will be in the list of protagonist's quests as 'taken'.
    User goes back to the list Actions.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    data = await state.get_data()
    cur_quest = data['cur_quest']
    cur_proto = get_proto_from_msg(message)
    if cur_proto.has_quest(cur_quest):
        return
    cur_proto.take_quest(cur_quest)
    await message.answer(tp.npc_quest_taken(cur_quest), parse_mode='HTML')
    await handler_talk_list_quests(message, state)


@router.message(FSM_Quest.process, F.text == 'Назад')
async def handler_quest_goback(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DESCRIPTION_NPC -> LIST_OF_QUESTS_NPC

    Calls after user don't want to take quest and returns
    to the list of quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await handler_talk_list_quests(message, state)


@router.message(FSM_Quest.process, F.text == 'Отдать предмет')
async def handler_quest_done_1(message: Message, state: FSMContext) -> None:
    """
    #TAKEN_QUEST_DESCRIPTION_NPC -> QUEST_DONE

    Calls after user has accomplished the 'bring' quest. quest will
    be removed from protagonist's list of quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    data = await state.get_data()
    cur_quest = data['cur_quest']
    cur_proto = get_proto_from_msg(message)
    if cur_quest.quest_type == QuestType.Bring and cur_proto.can_complete(cur_quest):
        await handler_quest_done(message, state)


@router.message(FSM_Quest.process, F.text == 'Отчитаться об убийстве')
async def handler_quest_done_2(message: Message, state: FSMContext) -> None:
    """
    #TAKEN_QUEST_DESCRIPTION_NPC -> QUEST_DONE

    Calls after user has accomplished the 'kill' quest. quest will
    be removed from protagonist's list of quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    data = await state.get_data()
    cur_quest = data['cur_quest']
    cur_proto = get_proto_from_msg(message)
    if cur_quest.quest_type == QuestType.Kill and cur_proto.can_complete(cur_quest):
        await handler_quest_done(message, state)


async def handler_quest_done(message: Message, state: FSMContext) -> None:
    """
    #TAKEN_QUEST_DESCRIPTION_NPC -> QUEST_DONE

    Calls after user has accomplished the quest. quest will
    be removed from protagonist's list of quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    data = await state.get_data()
    cur_quest = data['cur_quest']
    cur_npc = data['cur_npc']
    cur_proto = get_proto_from_msg(message)
    cur_npc.quests.remove(cur_quest)
    cur_proto.complete_quest(cur_quest)
    await message.answer(
        tp.npc_quest_done(cur_proto, cur_quest),
        reply_markup=kb.make_keyboard_congratulation(),
        parse_mode='HTML'
    )


@router.message(FSM_Quest.process, F.text == 'Отлично')
async def handler_quest_done_great(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DONE -> CONVERSATION

    Calls after user completes the quest. User is sent
    to the conversation stage.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.     
    """
    data = await state.get_data()
    cur_quest = data['cur_quest']
    if cur_quest.is_final:
        await message.answer(tp.game_completed(), reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        await state.set_state(FSM_End.completed)
    else:
        await handler_talk_choose_npc_main(message, state)


# Атаковать

@router.message(FSM_Location.choose_act, F.text == 'Осмотреть врага')
async def handler_inspect(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls after user wants to inspect enemies. Func display info 
    list of enemies.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_location = cur_proto.current_location
    if not cur_location.enemies:
        await message.answer(tp.no_enemies())
        return
    await message.answer(
        tp.who_to_attack(),
        reply_markup=kb.make_keyboard_attack_list(cur_location.enemies),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Attack.choose_enemy)


@router.message(FSM_Attack.choose_enemy, F.text == 'Отмена')
async def handler_inspect_cancel(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls when user wants to go back after seen list
    of enemies. User goes to current location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    await handler_location_start(message, state)


@router.message(FSM_Attack.choose_enemy)
async def handler_inspect_action(message: Message, state: FSMContext) -> None:
    """
    #LOCATION -> ENEMY_DESCIPTION

    Calls after user has inspected enemy. Func display info
    about enemy and gives choice: attack or go away.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_location = cur_proto.current_location
    cur_enemy = get_enemy_from_msg(cur_location, message.text)
    await state.set_state(FSM_Attack.descr)
    await state.update_data({'cur_enemy': cur_enemy})
    await handler_enemy_description(message, state)


async def handler_enemy_description(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION

    Calls after user has inspected enemy. Func display info
    about enemy and gives choice: attack or go away.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    data = await state.get_data()
    cur_enemy = data['cur_enemy']
    await send_photo_or_text(message, cur_enemy.image,
                             tp.inspect_enemy(cur_enemy), kb.make_keyboard_enemy_description())


@router.message(FSM_Attack.descr, F.text == 'Напасть')
async def handler_battle_start(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION -> BATTLE

    Calls after user is attacking enemy.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await state.update_data({
        'prev_msg_info': None,
        'msg_attack': None,
        'prev_msg_attack': None
    })
    await state.set_state(FSM_Battle.battle)
    await handler_battle_action(message, state)


@router.message(FSM_Attack.descr, F.text == 'Назад')
async def handler_description_cancel(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION -> LOCATION

    Calls after user is going away from enemy.
    User goes to the current location

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await handler_location_start(message, state)


async def handler_battle_action(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION

    Calls after user has inspected enemy. Func display info
    about enemy and gives choice: attack or go away.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    data = await state.get_data()
    cur_proto = get_proto_from_msg(message)
    cur_enemy = data['cur_enemy']
    msg = await message.answer(
        tp.battle(cur_proto, cur_enemy),
        reply_markup=kb.make_keyboard_battle(),
        parse_mode='HTML'
    )
    if message.text == 'Атаковать':
        if data.get('msg_attack'):
            if data.get('prev_msg_attack'):
                await data['prev_msg_attack'].delete()
            await state.update_data({'prev_msg_attack': data['msg_attack']})
        await data['prev_msg_info'].delete()
        await message.delete()
    await state.update_data({'prev_msg_info': msg})


@router.message(FSM_Battle.battle, F.text == 'Атаковать')
async def handler_battle_attack(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION -> BATTLE -> ENEMY_DESCRIPTION

    Calls after user is attacking enemy.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    data = await state.get_data()
    async with data['semaphore']:
        cur_proto = get_proto_from_msg(message)
        cur_enemy = data['cur_enemy']
        if cur_enemy.is_dead:
            return

        try:
            prota_roll, enemy_roll = cur_proto.attack(cur_enemy)
            msg = await message.answer(
                tp.attack_action(cur_proto, cur_enemy, prota_roll, enemy_roll),
                parse_mode='HTML'
            )
            await state.update_data({'msg_attack': msg})
            if cur_enemy.is_dead:
                await message.answer(
                    tp.enemy_defeated(cur_enemy),
                    reply_markup=kb.make_keyboard_congratulation(),
                    parse_mode='HTML'
                )
                if cur_enemy in cur_proto.current_location.enemies:
                    cur_proto.current_location.enemies.remove(cur_enemy)
                await state.set_state(FSM_Battle.congratulation)
                return
            await handler_battle_action(message, state)
        except ProtagonistDead:
            await handler_dead(message, state)


@router.message(FSM_Battle.battle, F.text == 'Сбежать')
async def handler_battle_attack(message: Message, state: FSMContext) -> None:
    """
    #ENEMY_DESCIPTION -> LOCATION

    Calls after user is going away from enemy.
    User goes to the current location

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    data = await state.get_data()
    cur_enemy = data['cur_enemy']
    await message.answer(
        tp.battle_run_off(cur_enemy),
        parse_mode='HTML'
    )
    await handler_location_start(message, state)


@router.message(FSM_Battle.congratulation, F.text == 'Отлично')
async def handler_battle_ended(message: Message, state: FSMContext) -> None:
    """
    #BATTLE -> LOCATION

    Calls after user clicked button after defeating enemy.
    User goes to the current location

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await handler_location_start(message, state)

# Отправиться

@router.message(FSM_Location.choose_act, F.text == 'Отправиться')
async def handler_go(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls after user wants to go to the another
    location. Func displays list of the adjacent locations.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_location = cur_proto.current_location
    
    await message.answer(
        tp.where_to_go(),
        reply_markup=kb.make_keyboard_directions_list(cur_location.directions, cur_proto),
        parse_mode='HTML'
    )
    
    await state.set_state(FSM_Location.where_to_go)


@router.message(FSM_Location.where_to_go, F.text == 'Отмена')
async def handler_go_where(message: Message, state: FSMContext) -> None:
    """
    #LOCATION

    Calls after user changed his mind about relocation.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    await handler_location_start(message, state)


@router.message(FSM_Location.where_to_go)
async def handler_go_where(message: Message, state: FSMContext) -> None:
    """
    #LOCATION -> (ANOTHER) LOCATION

    Calls after user has chosen new location.
    Protagonist moving to appropriate location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    
    cur_proto = get_proto_from_msg(message)
    cur_direction = get_direction_from_msg(cur_proto, message.text)
    if cur_direction and cur_direction.location_level <= cur_proto.level:
        await message.answer(
            tp.going(cur_direction),
            parse_mode='HTML'
        )
        cur_proto.go(cur_direction)
        await handler_location_start(message, state)


@router.message(FSM_Location.choose_act, F.text == 'Меню героя')
async def handler_protagonist_menu(message: Message, state: FSMContext) -> None:
    """
    #LOCATION -> PROTAGONIST_MENU

    Calls when user wants to see the menu.
    Func displays this menu.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await message.answer(
        tp.proto_menu(),
        reply_markup=kb.make_keyboard_protagonist_menu(),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Protagonist_Menu.process)


@router.message(FSM_Protagonist_Menu.process, F.text == 'Профиль героя')
async def handler_task_list(message: Message, state: FSMContext) -> None:
    """
    #PROTAGONIST_MENU

    Calls when user wants to see his profile.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    cur_proto = get_proto_from_msg(message)
    await message.answer(
        tp.proto_info(cur_proto),
        reply_markup=kb.make_keyboard_protagonist_menu(),
        parse_mode='HTML'
    )


@router.message(FSM_Protagonist_Menu.process, F.text == 'Список заданий')
async def handler_task_list(message: Message, state: FSMContext) -> None:
    """
    #PROTAGONIST_MENU -> LIST_OF_QUESTS_PROTAGONIST

    Calls when user wants to see list of taken quests.
    Func displays this quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    cur_proto = get_proto_from_msg(message)
    if not cur_proto.current_quests:
        await message.answer(tp.no_quests())
        return
    await message.answer(
        tp.proto_quests_list(cur_proto),
        reply_markup=kb.make_keyboard_proto_quest_list(
            cur_proto,
            cur_proto.current_quests
        ),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Protagonist_Menu.quest_description)


@router.message(FSM_Protagonist_Menu.process, F.text == 'Назад')
async def handler_task_list_descr_cancel(message: Message, state: FSMContext) -> None:
    """
    #PROTAGONIST_MENU -> LOCATION

    Calls after user wants to go back from viewing
    his quests. User goes back to current location.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    await handler_location_start(message, state)


@router.message(FSM_Protagonist_Menu.quest_description, F.text == 'Отмена')
async def handler_task_list_descr_cancel(message: Message, state: FSMContext) -> None:
    """
    #LIST_OF_QUESTS_PROTAGONIST -> PROTAGONIST_MENU

    Calls after user wants to go back from viewing
    his quests. User goes back to protagonist menu.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """
    await handler_protagonist_menu(message, state)


@router.message(FSM_Protagonist_Menu.quest_description)
async def handler_quest_descr(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DESCRIPTION_PROTAGONIST

    Calls after user has chosen quest in the list. Displays
    info about quest and one button: Go back.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    cur_proto = get_proto_from_msg(message)
    cur_quest = cur_proto.find_quest(message.text)
    await message.answer(
        tp.npc_quest(cur_quest),
        reply_markup=kb.make_keyboard_quest_description_back(),
        parse_mode='HTML'
    )
    await state.set_state(FSM_Protagonist_Menu.quest_process)
    await state.update_data({'cur_quest': cur_quest})


@router.message(FSM_Protagonist_Menu.quest_process, F.text == 'Назад')
async def handler_quest_goback(message: Message, state: FSMContext) -> None:
    """
    #QUEST_DESCRIPTION_PROTAGONIST -> LIST_OF_QUESTS_PROTAGONIST

    Calls after user wants to return to the list of quests.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await handler_task_list(message, state)


async def handler_dead(message: Message, state: FSMContext) -> None:
    """
    #DEAD

    Calls after protagonist is dead. Only option is to start
    again with /start command.

    :param message: All data about sent message from user.
    :param state: Current FSM Context.
    """

    await message.answer(tp.proto_dead(), parse_mode='HTML')
    await state.set_state(FSM_End.dead)
