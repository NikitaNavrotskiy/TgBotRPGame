# RPG Telegram Bot Game

This is an RPG (role-playing game) telegram bot where users can step into the shoes of a hero and embark on an epic adventure in a fantasy world.


## Recomemnded

Install `git-lfs` package before cloning to enable images.

Linux:
```
sudo apt install git-lfs
```

Macos:
```
brew instal git-lfs
```


## How to Play

1. Start a chat with the bot by searching for it on Telegram.
2. Begin your journey by creating a character with your name.
3. Explore the world and interact with NPCs (non-player characters) to receive quests and advance the story.
4. Engage in battles with enemies to obtain
   items and pass quests.
5. Raise the level of your character to improve his
   health and damage.


## Getting Started

1. Clone the repository.
2. Install the required dependencies by running 
   ```
   pip install -r requirements.txt
   ```
3. Generate database by executing
   ```
   python3 app/load_all.py
   ```
4. Get Telegram bot Token from BotFather: https://telegram.me/BotFather
5. Make Environment variable TG_TOKEN
   ```
   export TG_TOKEN=[Place_your_token_here]
   ```
6. Run the script.
   ```
   python3 app/run.py
   ```
7. Start interacting with the bot on Telegram by 
   sending `/start`.


## Walkthrough

Walkthrough for the game:
[Guide](Walkthrough.md)


## Technologies Used

- Python3
- Aiogram
- SQLAlchemy
- Sphinx


## Contributors

- Whistler
- Rufinakl
