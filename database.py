from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:12345678@localhost:3306/sayan" #dummy
engine = create_engine(db_url)
Session = sessionmaker(autocommit = False, autoflush=False, bind=engine)