from typing import List

from game import Direction, Enemy, NPC, Protagonist, Quest, QuestType


TemplateWelcome = """
<b>Добро пожаловать</b>, {name}!

Ваша цель в этой игре - выполнять задания, сражаться с монстрами и путешествовать по различным местам.

<b>Справка игры</b>

🎮 <b>Команды</b>
- <code>/start</code> - Начать игру (заново)

🛡️ <b>Действия</b>
- <b>Поговорить</b>: Начать диалог с персонажами на локации.
- <b>Осмотреть врага</b>: Участвовать в эпических битвах с врагами.
- <b>Отправиться</b>: Посетить другие локации.
- <b>Меню героя</b>: Информация о герое.

💬 <b>Разговор</b>
- <b>Взять задание</b>: Взять задание на выполнение.
- <b>[Завершить задание другого персонажа]</b>

⚔️ <b>Бой</b>
- <b>Атаковать</b>: Атаковать врага.
- <b>Сбежать</b>: Покинуть поле битвы.

🗺️ <b>Отправиться</b>
- <b>Выбрать открытую локацию для перемещения.</b>

🛍️ <b>Меню героя</b>
- <b>Профиль героя</b>: Информация о текущем уровне и характеристиках.
- <b>Список заданий</b>: Взятые на выполнение квесты.
"""


TemplateLocationNPC = "{available}<u>{name}</u>\n"


TemplateLocationEnemy = "       <u>{name}</u>  {level} ур.\n"


TemplateLocation = """
<b>Локация:</b> <u>{name}</u>

<b>Описание:</b> {description}
{npcs}{enemies}
"""

TemplateTalk = "С кем будем говорить?"


TemplateNoNPC = "На локации нет персонажей"


TemplateTalkNPCQuests = "Выберете задание"


TemplateNoQuests = "У вас нет заданий"


TemplateAttack = "Кто вас интересует?"


TemplateNoEnemies = "На локации нет врагов"


TemplateGo = "Куда отправимся?"


TemplateGoDirectly = "Отправляемся {name}"


TemplateTalkOrInspect = """
<b>{name}:</b>
    {description}

    \"{phrase}\""""


TemplateNPCQuest = """
<b>Задание:</b>
    {name}.
<b>Описаине:</b>
    {description}
"""


TemplateNPCQuestTaken = """
Задание <b>{name}</b> взято."""


TemplateNPCQuestDone = """
{congratulation}

Задание <b>{name}</b> выполнено!

Вы получили <b>{level} уровень</b>
Здоровье повысилоcь до <b>{health}</b>
Урон повысился до <b>{damage}</b>
{new_locations}"""


TemplateAttackAction = """
Ваш бросок: {proll} + {plevel} = <b>{presult}</b>
Бросок врага: {eroll} + {elevel} = <b>{eresult}</b>
{action_result}"""


TemplateAttackActionSuccess = """
    Вы бьёте врага на <b>{damage}</b> урона"""


TemplateAttackActionFailure = """
    Враг бьет вас на {damage} урона"""


TemplateAttackActionDraw = """
    Промах!"""


TemplateBattle = """
<b><u>{ename}</u></b> {elevel} ур.
<b>Здоровье:</b> {ehealth}🩸 || <b>Урон:</b> {edamage}⚔️
{ehealth_bar}

<b><u>{pname}</u></b> {plevel} ур.
<b>Здоровье:</b> {phealth}🩸 || <b>Урон:</b> {pdamage}⚔️
{phealth_bar}"""


TemplateBattleRunoff = "Вы сбежали от <b>{name}</b>"


TemplateEnemyDefeated = """
Поздравляем! Враг <b>{name}</b> побеждён!{items}"""


TemplateDead = "Вы умерли, <b>поздравляем!</b>"


TemplateCompleted = """
<b>Поздравляем!</b> Вы прошли игру!"""


TemplateProtagonistMenu = """
Выберите опцию"""


TemplateProtagonistInfo = """
<b>Профиль</b>
<code>Имя:          </code><b>{name}</b>
<code>Уровень:      </code><b>{level}</b>
<code>Здоровье:     </code><b>{health}</b>/<b>{max_health}</b>
<code>Урон:         </code><b>{damage}</b>
<code>Предметы:     </code>{inventory}
<code>Убитые враги: </code>{killed_enemies}"""


def template_welcome(prota: Protagonist) -> str:
    """
    Filling template for welcome message.

    :param prota: Protagonist.
    :return: Filled template.
    """

    return TemplateWelcome.format(
        name=prota.name
    )


def npc_info(npcs: List[NPC], cur_proto: Protagonist) -> str:
    """
    Filling template that describe npcs 
    on the location.

    :param npcs: List of npcs.
    :param cur_proto: Protagonist.
    :return: Filled template.
    """

    res = ''
    if npcs:
        res = '\n<b>Персонажи:</b>\n'

    for npc in npcs:
        emoji = ''
        if cur_proto.npc_has_quests_to_complete(npc):
            emoji = '❔'
        elif cur_proto.npc_has_not_taken_quests(npc):
            emoji = '📜'
        res += TemplateLocationNPC.format(
            name=npc.name,
            available=f'{emoji} ' if emoji else '       '
        )

    return res


def enemies_info(enemies: List[Enemy]) -> str:
    """
    Filling template that describe enemies
    on the location.

    :param enemies: List of enemies.
    :return: Filled template.
    """

    res = ''
    if enemies:
        res = '\n<b>Враги:</b>\n'

    for enemy in enemies:
        res += TemplateLocationEnemy.format(
            name=enemy.name,
            level=enemy.level
        )

    return res


def location_info(loc_name: str, loc_descr: str, 
                  npcs: List[NPC], enemies: List[Enemy], cur_proto: Protagonist) -> str:
    """
    Filling template that describe location.

    :param loc_name: Current location's name.
    :param loc_descr: Current location's description.
    :param npcs: List of npcs.
    :param enemies: List of enemies.
    :param cur_proto: Protagonist.
    :return: Filled template.
    """

    return TemplateLocation.format(
        name=loc_name,
        description=loc_descr,
        enemies=enemies_info(enemies),
        npcs=npc_info(npcs, cur_proto)
    )


def no_npc() -> str:
    """
    Returns phrase when there is no
    npc to talk.

    :return: Message string.
    """

    return TemplateNoNPC


def no_enemies() -> str:
    """
    Returns phrase when there is no
    enemy to attack.

    :return: Message string.
    """

    return TemplateNoEnemies


def no_quests() -> str:
    """
    Returns phrase when there is no
    quests in the list.

    :return: Message string.
    """

    return TemplateNoQuests


def talk_with() -> str:
    """
    Returns phrase when choosing
    npc to talk.

    :return: Message string.
    """

    return TemplateTalk


def who_to_attack() -> str:
    """
    Returns phrase when choosing
    enemy to attack.

    :return: Message string.
    """

    return TemplateAttack


def where_to_go() -> str:
    """
    Returns phrase when choosing
    way to go.

    :return: Message string.
    """

    return TemplateGo


def going(direction: Direction) -> str:
    """
    Filling template that describe way
    user relocate.

    :param direction: Direction instance to go.
    :return: Filled template.
    """

    return TemplateGoDirectly.format(
        name=direction.name
    )


def talk_with_npc(npc: NPC) -> str:
    """
    Filling template that describe npc.

    :param npc: NPC instance to talk with.
    :return: Filled template.
    """

    return TemplateTalkOrInspect.format(
        name=npc.name,
        description=npc.description,
        phrase=npc.phrase
    )


def inspect_enemy(enemy: Enemy) -> str:
    """
    Filling template that describe npc.

    :param enemy: Enemy instance to talk with.
    :return: Filled template.
    """

    return TemplateTalkOrInspect.format(
        name=enemy.name,
        description=enemy.description,
        phrase=enemy.phrase
    )


def talk_npc_actions() -> str:
    """
    Returns phrase when choosing
    a quest.

    :return: Message string.
    """

    return TemplateTalkNPCQuests


def npc_quest(quest: Quest) -> str:
    """
    Filling template that describe quest.

    :param quest: Quest to describe.
    :return: Filled template.
    """

    return TemplateNPCQuest.format(
        name=quest.name,
        description=quest.description
    )


def npc_quest_taken(quest: Quest) -> str:
    """
    Filling template message after
    user has taken a quest.

    :param quest: Taken quest.
    :return: Filled template.
    """

    return TemplateNPCQuestTaken.format(
        name=quest.name
    )


def npc_quest_done(prota: Protagonist, quest: Quest) -> str:
    """
    Filling template message after
    completing quest.

    :param prota: Protagonist
    :param quest: Completed quest.
    :return: Filled template.
    """

    locations = prota.new_locations()
    new_locations = ''
    if locations:
        new_locations = '\nДоступны новые локации:'
        for location in locations:
            new_locations += f'\n    <b>{location}</b>'
    return TemplateNPCQuestDone.format(
        congratulation=quest.congratulation,
        name=quest.name,
        level=prota.level,
        health=prota.hp,
        damage=prota.damage,
        new_locations=new_locations
    )


def generate_health_bar(hp: int, max_hp: int):
    green_value: int = max(min(int(hp / max_hp * 100 // 10), 10), 0)
    return '🟩' * green_value + '🟥' * (10 - green_value)


def battle(prota: Protagonist, enemy: Enemy) -> str:
    """
    Filling template that
    describes enemy's condition.

    :param prota: Protagonist
    :param enemy: Enemy
    :return: Filled template.
    """

    return TemplateBattle.format(
        ename=enemy.name,
        elevel=enemy.level,
        ehealth=enemy.hp,
        edamage=enemy.damage,
        ehealth_bar=generate_health_bar(enemy.hp, enemy.max_hp),
        pname=prota.name,
        plevel=prota.level,
        phealth=prota.health(),
        pdamage=prota.damage,
        phealth_bar=generate_health_bar(prota.health(), prota.level * 10)
    )


def attack_action(prota: Protagonist, enemy: Enemy, prota_roll: int, enemy_roll: int) -> str:
    """
    Filling template message after
    attack action.

    :param prota: User's protagonist.
    :param enemy: Enemy to attack.
    :param prota_roll: Protagonist's roll.
    :param enemy_roll: Enemy's roll.
    :return: Filled template.
    """

    if enemy_roll > prota_roll:
        action_result = TemplateAttackActionFailure.format(damage=enemy.damage)
    elif prota_roll > enemy_roll:
        action_result = TemplateAttackActionSuccess.format(damage=prota.damage)
    else:
        action_result = TemplateAttackActionDraw
   
    return TemplateAttackAction.format(
        proll=prota_roll - prota.level, plevel=prota.level, presult=prota_roll,
        eroll=enemy_roll - enemy.level, elevel=enemy.level, eresult=enemy_roll,
        action_result=action_result
    )


def battle_run_off(enemy: Enemy) -> str:
    """
    Filling template message after
    run away action.

    :param enemy: Enemy user has battle with.
    :return: Filled template.
    """

    return TemplateBattleRunoff.format(
        name=enemy.name
    )


def enemy_defeated(enemy: Enemy) -> str:
    """
    Filling template message after
    enemy has been defeated.

    :param enemy: Enemy that was defeated.
    :return: Filled template.
    """

    items = ''
    if enemy.items:
        items = '\n\nВы получили:'
        for item in enemy.items:
            items += f'\n    {item}'

    return TemplateEnemyDefeated.format(
        name=enemy.name,
        items=items
    )


def proto_menu() -> str:
    """
    Asking player to choose menu option.

    :return: Filled template.
    """

    return TemplateProtagonistMenu


def proto_quests_list(prota: Protagonist) -> str:
    """
    Filling template that describes
    list of protagonist's quests.

    :param prota: User's protagonist.
    :return: Filled template.
    """

    res = '<b>Список заданий:</b>\n'
    
    for quest in prota.current_quests:
        text = f'    {quest.name}'
        match quest.quest_type:
            case QuestType.Kill:
                text += ' ⚔️'
            case QuestType.Bring:
                text += ' 💍'
            case QuestType.Talk:
                text += ' 💬'
        res += text + '\n'

    return res


def proto_dead() -> str:
    """
    Returns message after dying.

    :return: Message string.
    """

    return TemplateDead


def game_completed() -> str:
    """
    Returns message after game completion

    :return: Message string
    """

    return TemplateCompleted


def proto_info(prota: Protagonist) -> str:
    """
    Filling template that describes
    info about protagonist.

    :param prota: User's protagonist.
    :return: Filled template.
    """

    killed_enemies = ''
    inventory = ''
    for item in prota.inventory.items():
        inventory += f'\n<code>    </code><b>{item[0]}</b>' * item[1]
    for enemy in prota.get_killed_enemies():
        killed_enemies += f'\n<code>    </code><b>{enemy}</b>'
    return TemplateProtagonistInfo.format(
        name=prota.name,
        level=prota.level,
        damage=prota.damage,
        health=prota.health(),
        max_health=prota.level * 10,
        inventory=inventory,
        killed_enemies=killed_enemies
    )
