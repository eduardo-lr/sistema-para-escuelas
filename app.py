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
    profesores = relationship('Horario', back_populates='curso')
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
    cursos = relationship('Horario', back_populates='profesor')

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
    
    profesor = relationship("Profesor", back_populates="cursos")
    curso = relationship("Curso", back_populates="profesores")

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
            hora = str(self.hora)
            minutos = str(self.minutos)
            if len(hora) == 1:
                hora = '0' + hora
            if len(minutos) == 1:
                minutos = minutos + '0'
            return hora + ":" + minutos 

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

    def __str__(self):
        return "{}, de las {} horas a las {} horas".format(self.dia, self.hora_inicial, self.hora_final) 

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

	def __str__(self):
		return self.dia

engine = create_engine('sqlite:///escuela.db')
metadata = Base.metadata
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Ahora poblamos las bases de datos.

# Creamos primero algunos alumnos y los agregamos.
Otto = Alumno("Otto", "Webber")
Diego = Alumno("Diego Armando", "Glagovsky")
Eduardo = Alumno("Eduardo", "Rodríguez", "Pérez")
Marco = Alumno("Marco Antonio", "Juarez", "Borja")
session.add_all([Otto, Diego, Eduardo, Marco])

# Agregamos algunos cursos.
algebra = Curso("Álgebra")
geometria = Curso("Geometría")
economia = Curso("Economía")
session.add_all([algebra, geometria, economia])

# Asignamos ahora algunos alumnos a los cursos
Otto.curso = algebra
Diego.curso = algebra
Eduardo.curso = geometria
Marco.curso = economia

# Agregamos los dìas de la semana.
lunes = Cdia("Lunes")
martes = Cdia("Martes")
miercoles = Cdia("Miércoles")
jueves = Cdia("Jueves")
viernes = Cdia("Viernes")
sabado = Cdia("Sábado")
domingo = Cdia("Domingo")
session.add_all([lunes, martes, miercoles, jueves, viernes, sabado, domingo])

# Agregamos algunos profesores.
Albert = Profesor("Albert", "Einstein")
Joseph = Profesor("Joseph", "Mupbala", "Khan")
session.add_all([Albert, Joseph])

# Asignamos cursos a los profesores.
h1 = Horario("12:00", "13:00")
h1.curso, h1.dia = algebra, martes
Albert.cursos.append(h1)

h2 = Horario("5:00", "6:00")
h2.curso, h2.dia = algebra, lunes
Joseph.cursos.append(h2)

h3 = Horario("11:30", "12:30")
h3.curso, h3.dia = geometria, miercoles
Joseph.cursos.append(h3)

h4 = Horario("9:15", "10:15")
h4.curso, h4.dia = economia, sabado
Joseph.cursos.append(h4)

def exportaInscritos():
	s = "{\n"
	cursos = session.query(Curso)
	for n, curso in enumerate(cursos):		
		s += "\t\"{}\": [".format(curso.nombre)
		alumnos = session.query(Alumno).where(Alumno.curso==curso).all()
		for m, alumno in enumerate(alumnos):
			s += "\"{}\"".format(str(alumno))
			if m != len(alumnos) - 1:
				s += ", "
			else:
				s += "]"
				if n != len([x for x in cursos]) - 1:
					s += ","
				s+= "\n"
	s += "}\n"		
	return s

def exportaHorarioProfesores():
	s = "{\n"
	profesores = session.query(Profesor)
	for n, profesor in enumerate(profesores):		
		s += "\t\"{}\": [".format(profesor.nombre)
		for m, horario in enumerate(profesor.cursos):
			s += "\"{}\"".format(str(horario))
			if m != len(profesor.cursos) - 1:
				s += ", "
			else:
				s += "]"
				if n != len([x for x in profesores]) - 1:
					s += ","
				s+= "\n"
	s += "}\n"		
	return s

def exportaHorarioCurso():
	s = "{\n"
	ext_query = session.query(Curso)
	for curso in ext_query:		
		s += "\t\"{}\": [".format(curso.nombre)
		query = session.query(Horario).where(Horario.curso == curso).all()
		for m, horario in enumerate(query):
			s += "\"{}\"".format(str(horario))
			if m != len(query) - 1:
				s += ", "
			else:
				s += "],\n"
	s += "}\n"		
	return s

print(exportaInscritos())
print(exportaHorarioProfesores())
print(exportaHorarioCurso())

session.close()
