from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
import sys

class FormatoInvalido(Exception): pass

class HorarioInvalido(Exception): pass

def _nombre_toString(nombre, app, apm=None):
    s = nombre + " " + app
    if apm:
        s += " " + apm
    return s

Base = declarative_base()

class Alumno(Base):
    
    __tablename__ = 'alumno'
    
    id_alumno = Column(Integer, Sequence('id_alumno_sequence'), primary_key=True)
    nombre = Column(String, nullable=False)
    app = Column(String, nullable=False)
    apm = Column(String)
    id_curso = Column(Integer, ForeignKey('curso.id_curso'))
    curso = relationship('Curso', back_populates='alumnos')

    def __init__(self, nombre, app, apm=None):
        self.nombre = nombre
        self.app = app
        self.apm = apm

    def __str__(self):
        return _nombre_toString(self.nombre, self.app, self.apm)

class Curso(Base):

    __tablename__ = 'curso'

    id_curso = Column(Integer, Sequence('id_curso_sequence'), primary_key=True)
    nombre = Column(String, nullable=False)
    profesores = relationship('Profesor', secondary='horario', back_populates='cursos')
    alumnos = relationship('Alumno', back_populates='curso')

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Profesor(Base):
    
    __tablename__ = 'profesor'
    
    id_profesor = Column(Integer, Sequence('id_profesor_sequence'), primary_key=True)
    nombre = Column(String, nullable=False)
    app = Column(String, nullable=False)
    apm = Column(String)
    cursos = relationship('Curso', secondary='horario', back_populates='profesores')

    def __init__(self, nombre, app, apm=None):
        self.nombre = nombre
        self.app = app
        self.apm = apm

    def __str__(self):
        return _nombre_toString(self.nombre, self.app, self.apm)

class Horario(Base):

    __tablename__ = 'horario'

    hora_final = Column(String, nullable=False)
    hora_inicial = Column(String, nullable=False)
    id_curso = Column(Integer, ForeignKey('curso.id_curso'), primary_key=True)
    id_profesor = Column(Integer, ForeignKey('profesor.id_profesor'), primary_key=True)
    id_dia = Column(Integer, ForeignKey('cdia.id_dia'))
    dia = relationship('Cdia', back_populates='horarios')
    
    class Hora:

        def __init__(self, string):
            try:
                self.hora, self.minutos = self._valida_hora(string)
            except FormatoInvalido as e:
                sys.exit(e)

        def __le__(self, other):
            eq = self.hora == other.hora and self.minutos == other.minutos
            le = self.hora < other.hora or (self.hora == other.hora and self.minutos < other.minutos)
            return eq or le

        def __str__(self):
            return str(self.hora) + ":" + str(self.minutos)

        def _valida_hora(self, string):
            import re
            if not re.fullmatch('\d{1,2}:\d{2}', string):
                raise FormatoInvalido("El formato de hora debe ser de 24 horas y de la forma 00:00")
            split_hora = string.split(":")
            hora = int(split_hora[0])
            minutos = int(split_hora[1])
            if hora >= 24 or minutos > 59:
                raise FormatoInvalido("Hora invalida")
            return hora, minutos

    def __init__(self, hora_inicial, hora_final):
        inicial = self.Hora(hora_inicial)
        final = self.Hora(hora_final)	
        try:
            self._verifica_horario(inicial, final)
        except HorarioInvalido as e:
            sys.exit(e)

        self.hora_inicial = str(inicial)
        self.hora_final = str(final)

    def _verifica_horario(self, inicial, final):
       if final <= inicial:
            raise HorarioInvalido("La hora final no puede ser menor o igual que la inicial")

class Cdia(Base):

	__tablename__ = 'cdia'
	
	id_dia = Column(Integer, Sequence('id_dia_sequence'), primary_key=True)
	dia = Column(String, nullable=False, unique=True)
	horarios = relationship('Horario', back_populates='dia')

	def __init__(self, dia):
		self.dia = dia

engine = create_engine('sqlite:///escuela.db')
metadata = Base.metadata
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Ahora poblamos las bases de datos.
# Agregamos primero algunos alumnos.
session.add_all([
	Alumno("Juan", "Domínguez", "Hernández"),
	Alumno("Diego Armando", "Sanchez", "Juarez"),
	Alumno("Eduardo", "Rodríguez", "Pérez"),
	Alumno("Marco Antonio", "Juarez", "Borja")])

# Agregamos algunos cursos.
session.add_all([
	Curso("Álgebra"),
	Curso("Geometría"),
	Curso("Economía")])

# Agregamos los dìas de la semana.
session.add_all([
	Cdia("Lunes"),
	Cdia("Martes"),
	Cdia("Miércoles"),
	Cdia("Jueves"),
	Cdia("Viernes"),
	Cdia("Sábado"),
	Cdia("Domingo")])

# Agregamos algunos profesores.
session.add_all([
	Profesor("Albert", "Einstein"),
	Profesor("Joseph", "Mupbala")])

session.close()
