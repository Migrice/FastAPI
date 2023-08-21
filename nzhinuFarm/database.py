from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nzhinuFarm.config import settings

engine = create_engine(settings.db_url)

#chaque instance de sessionLocal sera une instance de la session de la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#On va utiiser cette classe Base pour la creation des modeles ORM
Base = declarative_base()