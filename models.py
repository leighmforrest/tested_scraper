from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://sqla')
Base = declarative_base()
Session = sessionmaker(bind=engine)
