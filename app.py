from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()
engine = create_engine('sqlite:///escuela.db')

class Alumno(Base):
    
    __tablename__ = 'alumno'
    
    id_alumno = Column(Integer, Sequence('id_alumno_sequence'), primary_key=True)
    nombre = Column(String, nullable=False)
    app = Column(String, nullable=False)
    apm = Column(String)

    def __init__(self, nombre, app, apm=None):
        self.nombre = nombre
        self.app = app
        self.apm = apm

    def __str__(self):
        s = self.nombre + " " + self.app
        if self.apm:
            s += " " + self.apm
        return s

class Curso(Base):

    __tablename__ = 'curso'

    id_curso = Column(Integer, Sequence('id_curso_sequence'), primary_key=True)
    nombre = Column(String, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Profesor(Base):
    
    __tablename__ = 'profesor'
    
    id_profesor = Column(Integer, Sequence('id_profesor'), primary_key=True)
    nombre = Column(String, nullable=False)
    app = Column(String, nullable=False)
    apm = Column(String)

    def __init__(self, nombre, app, apm=None):
        self.nombre = nombre
        self.app = app
        self.apm = apm

    def __str__(self):
        s = self.nombre + " " + self.app
        if self.apm:
            s += " " + self.apm
        return s
