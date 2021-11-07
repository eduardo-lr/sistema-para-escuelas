from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship 

Base = declarative_base()
engine = create_engine('sqlite:///escuela.db')

class FormatoInvalido(Exception): pass

class HorarioInvalido(Exception): pass

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

horarios = Table('horarios', Base.metadata,
            Column('id_curso', ForeignKey('curso.id_curso'), primary_key=True),
            Column('id_profesor', ForeignKey('profesor.id_profesor'), primary_key=True))

class Horario(Base):

    __tablename__ = 'horario'

    id_horario = Column(Integer, Sequence('id_horario_sequence'), primary_key=True)
    hora_final = Column(String, nullable=False)
    hora_inicial = Column(String, nullable=False)

    def __init__(self, hora_inicial, hora_final):
        inicial = Hora(hora_inicial)
        final = Hora(hora_final)
        try:
            if final <= inicial:
                raise HorarioInvalido("La hora final no puede ser menor o igual que la inicial")
        except HorarioInvalido as e:
            print(e)


class Hora:

    def __init__(self, string):
        def _valida_hora(string):
            import re
            if not re.fullmatch('\d{1,2}:\d{2}', string):
                raise FormatoInvalido("El formato de hora debe ser de 24 horas y de la forma 00:00")
            split_hora = string.split(":")
            hora = int(split_hora[0])
            minutos = int(split_hora[1])
            if hora >= 24 or minutos > 59:
                raise FormatoInvalido("Hora invalida")
            return hora, minutos

        try:
            self.hora, self.minutos = _valida_hora(string)
        except FormatoInvalido as e:
            print(e)

    def __le__(self, other):
        eq = self.hora == other.hora and self.minutos == other.minutos
        le = self.hora < other.hora or (self.hora == other.hora and self.minutos < other.minutos)
        return eq or le

    def __str__(self):
        return str(self.hora) + ":" + str(self.minutos)

Horario('11:00', '13:30')