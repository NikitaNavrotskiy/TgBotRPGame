# План состояний игры
Название каждого состояния обозначены заголовками

Текст сообщения бота обозначен цитатой:
>Текст сообщения

Переход на состояние описан как:

[Действие] -> [#Название_состояния](#Название_состояния)

Также с помощью `[]` описаны переменные Python, например, `[location.name]`


## /start 
> `[START_MESSAGE]`
>
> Введите имя игрока:

[Пользователь пишет `protagonist.name`] -> [#Добро_пожаловать](#добро_пожаловать)

## Добро_пожаловать
`[protagonist]`

> `[WELCOME_MESSAGE.format(protagonist.name)]`

tg кнопки:

`[Начать игру]` -> [#Локация](#локация)

## Локация
`[location]`

> `[location.name]`
> `[location.description]`
>
> NPC на локации:
>>    `[location.npc[0].name]`📜((если есть квест))
>>
>>    `[location.npc[1].name]`
>
> Враги на локации:
>>    `[location.enemies[0].name]` `[location.enemies[0].level]` ур.
>>
>>    `[location.enemies[1].name]` `[location.enemies[1].level]` ур.

tg кнопки:

`[Поговорить]` ->
>    `[Поговорить с location.npc[0].name]` -> [#Разговор](#разговор)
> 
>    `[Поговорить с location.npc[1].name]` -> [#Разговор](#разговор)
> 
>    `[Отмена]`
  
`[Осмотреть врага]` ->
>    `[location.enemies[0].name]` -> [#Описание_врага](#описание_врага)
> 
>    `[location.enemies[1].name]` -> [#Описание_врага](#описание_врага)
> 
>    `[Отмена]`

`[Отправиться]` ->
>    `[location.directions[0].name]` -> [#Локация](#локация)
> 
>    `[location.directions[1].name]` -> [#Локация](#локация)
> 
>    `[Отмена]`

`[Список заданий]` -> [#Список_квестов_protagonist](#список_квестов_protagonist)

## Разговор
`[npc]`

> `[npc.name]`
> 
> `[npc.phrase]`

tg кнопки:

`[Список заданий]` -> [#Список_квестов_npc](#список_квестов_npc)

*`[Передать сообщение от quest.npc.name]` -> [#Квест_выполнен](#квест_выполнен)

`[Отмена]` -> [#Локация](#Локация)

## Описание_врага
`[enemy]`

> `[enemy.name]`
> 
> Уровень: `[enemy.level]`
> 
> Здоровье: `[enemy.health]`🩸
> 
> Урон: `[enemy.damage]`⚔️

tg кнопки:

`[Напасть]` -> [#Сражение](#сражение)

`[Отмена]` -> [#Локация](#локация)

## Сражение
`[enemy]`

> `[enemy.name]` `[enemy.level]` ур.
> 
> `[enemy.health]`🩸 || `[enemy.damage]`⚔️

tg кнопки:

`[Атаковать]` -> [#Атака](#атака)

`[Сбежать]` -> [#Локация](#локация)

## Атака
`[enemy]`

> `[protagonist.attack(enemy)[0]]` ⚔️ `[protagonist.attack(enemy)[1]]`
> 
> Вы бьёте врага на `[protagonist.damage]` урона

[Враг жив] -> [#Сражение](#сражение)

[Враг мертв] -> [#Победа](#победа)

## Победа
`[enemy]`

> [enemy.name] побежден!
> 
> Вы получили:
> 
>>    enemy.items[0].name
>>
>>    1 уровень

tg кнопки:

`[Отлично]` -> [#Локация](#локация)

## Список_квестов_protagonist
`[protagonist]`

> `[protagonist.current_quests[0].name]`⚔️
> 
> `[protagonist.current_quests[1].name]`💬
> 
> `[protagonist.current_quests[2].name]`💍

tg кнопки:

`[protagonist.current_quests[0].name]` -> [#Описание_квеста_protagonist](#описание_квеста_protagonist)

`[protagonist.current_quests[1].name]` -> [#Описание_квеста_protagonist](#описание_квеста_protagonist)

`[protagonist.current_quests[2].name]` -> [#Описание_квеста_protagonist](#описание_квеста_protagonist)

`[Отмена]` -> [#Локация](#локация)

## Список_квестов_npc
`[npc]`

> `[npc.quests[0].name]`⚔️
> 
> `[npc.quests[1].name]`💬 (взято)
> 
> `[npc.quests[2].name]`💍

tg кнопки:

`[protagonist.quests[0].name]` -> [#Описание_квеста_npc](#описание_квеста_npc)

`[protagonist.quests[1].name]` -> [#Описание_взятого_квеста_npc](#описание_взятого_квеста_npc)

`[protagonist.quests[2].name]` -> [#Описание_квеста_npc](#описание_квеста_npc)

`[Отмена]` -> [#Разговор](#разговор)

## Описание_квеста_protagonist
`[quest]`

> `[quest.name]`
> 
> `[quest.description]`

tg кнопки:

`[Назад]` -> [#Список_квестов_protagonist](#список_квестов_protagonist)

## Описание_квеста_npc
`[quest]`

> `[quest.name]`
> 
> `[quest.description]`

tg кнопки:

`[Взять задание]` -> [#Список_квестов_npc](#список_квестов_npc)

`[Назад]` -> [#Список_квестов_npc](#список_квестов_npc)

## Описание_взятого_квеста_npc
`[quest]`

> `[quest.name]`
> 
> `[quest.description]`

tg кнопки:

*`[Отдать предмет | Отчитаться об убийстве]` -> [#Квест_выполнен](#квест_выполнен)

`[Назад]` -> [#Список_квестов_npc](#список_квестов_npc)

## Квест_выполнен
`[quest]`

> `[quest.congratulation]`
> 
> Задание `[quest.name]` выполнено!
> 
> Вы получили 1 уровень

tg кнопки:

`[Отлично]` -> [#Разговор](#разговор)
