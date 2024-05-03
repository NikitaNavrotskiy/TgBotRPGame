from .schemas import QuestType, Base, Location, Direction, NPC, Enemy, Item, Quest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = 'main.db'

engine = create_engine(f'sqlite:///{DB_NAME}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
