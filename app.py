from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class Alumno(Base):
    
    __tablename__ = 'alumno'
    
    id_alumno = Column(Integer, Sequence('id_alumno_sequence'), primary_key=True)   
