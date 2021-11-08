from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
import sys

class Persona:
    """ Clase para abstraer el comportamiento de alumnos y profesores.
    """

    def __init__(self, nombre, app, apm=None):
        """ Constructor de la clase Persona. La persona puede o no
		    tener apellido materno. 
        
        Args:
          nombre: El nombre de la persona
          app: El apellido paterno de la persona
          apm: El apellido materno de la persona. Por default es None.
        """
        self.nombre = nombre
        self.app = app
        self.apm = apm

    def __str__(self):
        """ Convierte el nombre de una persona en una cadena. 

        Returns:
          s: Una cadena con el nombre de la persona.
        """
        s = self.nombre + " " + self.app
        if self.apm:
            s += " " + self.apm
        return s
        

# Creamos una clase para heredar e implementar el mapeo objeto relacion en SQLAlchemy
Base = declarative_base()

class Alumno(Base, Persona):
    """ Clase para modelar alumnos. La clase extiende a Persona y Base.
    """    

    " El nombre de la tabla en el ORM."
    __tablename__ = 'alumno'
    " El id del alumno. La columna es llave primaria y autoincrementable."
    id_alumno = Column(Integer, Sequence('id_alumno_sequence'), primary_key=True)
    " El nombre del alumno. La columna no admite valores nulos"
    nombre = Column(String, nullable=False)
    " El apellido paterno del alumno. La columna no admite valores nulos."
    app = Column(String, nullable=False)
    " El apellido materno del alumno."
    apm = Column(String)
    " Llave foranea para referenciar el curso al cual se inscribe el alumno."
    id_curso = Column(Integer, ForeignKey('curso.id_curso'))
    " Relación para vincular las clases Curso y Alumno."
    curso = relationship('Curso', back_populates='alumnos')

    def __init__(self, nombre, app, apm=None):
        """ Constructor de la clase Alumno. Un alumno puede o no
            tener apellido materno.

        Args:
          nombre: El nombre de la persona
          app: El apellido paterno de la persona
          apm: El apellido materno de la persona. Por default es None.
        """
        Persona.__init__(self, nombre, app, apm)

    def __str__(self):
        """ Convierte el nombre de un alumno en una cadena. 

        Returns:
          s: Una cadena con el nombre del alumno.
        """
        return Persona.__str__(self)

class Profesor(Base, Persona):
    """ Clase para modelar profesores. La clase extiende a Persona y Base.
    """    

    " El nombre de la tabla en el ORM."    
    __tablename__ = 'profesor'
    " El id del profesor. La columna es llave primaria y autoincrementable."    
    id_profesor = Column(Integer, Sequence('id_profesor_sequence'), primary_key=True)
    " El nombre del profesor. La columna no admite valores nulos"
    nombre = Column(String, nullable=False)
    " El apellido paterno del profesor. La columna no admite valores nulos."
    app = Column(String, nullable=False)
    " El apellido materno del profesor."
    apm = Column(String)
    " Relación para vincular las clases Curso y Profesor, por medio de Horario."
    cursos = relationship('Horario', back_populates='profesor')

    def __init__(self, nombre, app, apm=None):
        """ Constructor de la clase Alumno. Un alumno puede o no
            tener apellido materno.

        Args:
          nombre: El nombre de la persona
          app: El apellido paterno de la persona
          apm: El apellido materno de la persona. Por default es None.
        """
        Persona.__init__(self, nombre, app, apm)

    def __str__(self):
        """ Convierte el nombre de un alumno en una cadena. 

        Returns:
          s: Una cadena con el nombre del alumno.
        """
        return Persona.__str__(self)

class Curso(Base):
    """ Clase para modelar cursos. La clase extiende a Base.
    """    

    " El nombre de la tabla en el ORM."
    __tablename__ = 'curso'
    " El id del profesor. La columna es llave primaria y autoincrementable."   
    id_curso = Column(Integer, Sequence('id_curso_sequence'), primary_key=True)
    " El nombre del curso. La columna no admite valores nulos"
    nombre = Column(String, nullable=False)
    " Relación para vincular las clases Profesor y Curso, por medio de Horario"
    profesores = relationship('Horario', back_populates='curso')
    " Relación para vincular las clases Alumno y Curso."
    alumnos = relationship('Alumno', back_populates='curso')

    def __init__(self, nombre):
        """ Constructor de la clase curso.

        Args:
          nombre: el nombre del curso.
        """
        self.nombre = nombre

    def __str__(self):
        """ Convierte el curso en una cadena. 

        Returns:
          Una cadena con el nombre del alumno.
        """
        return self.nombre

class Horario(Base):
    """ Clase para modelar horarios. La clase extiende a Base.
    """    
    " El nombre de la tabla en el ORM."
    __tablename__ = 'horario'
    " La hora final del horario. La columna no admite valores nulos."
    hora_final = Column(String, nullable=False)
    " La hora inicial del horario. La columna no admite valores nulos."
    hora_inicial = Column(String, nullable=False)
    " Llave foranea para referenciar el curso al cual está vinculado el horario."
    id_curso = Column(Integer, ForeignKey('curso.id_curso'), primary_key=True)
    " Relacion para vincular las tablas curso y Profesor."
    curso = relationship("Curso", back_populates="profesores")
    " Llave foranea para referenciar el profesor al cual está vinculado el horario."
    id_profesor = Column(Integer, ForeignKey('profesor.id_profesor'), primary_key=True)
    " Relacion para vincular las tablas Profesor y Curso."
    profesor = relationship("Profesor", back_populates="cursos")
    " Llave foranea para refenciar el dia correspondiente al horario."  
    id_dia = Column(Integer, ForeignKey('cdia.id_dia'))
    " Relacion para vincular las tablas Cdia y Horario." 
    dia = relationship('Cdia', back_populates='horarios')
    
    class Hora:
        """ Clase interna para modelar objetos hora de la forma '00:00'
        """

        class FormatoInvalido(Exception): 
            """ Clase para implementar excepciones en el formato con el que el usuario ingresa una hora.
            """
            pass

        def __init__(self, string):
            """ Constructor de la clase Hora.

            Args:
              hora: La hora entre 0 y 23 del objeto Hora.
              minutos: Los minutos entre 0 y 59 del objeto Hora.
            """
            try:
                self.hora, self.minutos = self._valida_hora(string)
            except FormatoInvalido as e:
                sys.exit(e)

        def __le__(self, other):
            """ Implementacion del operador de comparacion '<=' para objetos Hora.
            Args:
               other: El objeto hora con el cual comparar.
            """
            eq = self.hora == other.hora and self.minutos == other.minutos
            le = self.hora < other.hora or (self.hora == other.hora and self.minutos < other.minutos)
            return eq or le

        def __str__(self):
            """ Convierte el objeto Hora en una cadena. 

            Returns:
              Una representacion en cadena del objeto Hora.
            """
            hora = str(self.hora)
            minutos = str(self.minutos)
            if len(hora) == 1:
                hora = '0' + hora
            if len(minutos) == 1:
                minutos = minutos + '0'
            return hora + ":" + minutos 

        def _valida_hora(self, string):
            """ Método auxiliar para validar que la cadena a convertir en un objeto Hora
                tenga un formato válido.

            Args:
              string: la cadena candidata a convertirse en un objeto Hora. 

            Returns:
              hora: Un entero entre 0 y 23 con la hora asociada al objeto Hora.
              minutos: Un entero entre 0 y 59 con los minutos asociados al objeto Hora.

            Raises:
              FormatoInvalido: Si la cadena no es de la forma 00:00 o no es una hora válida.
            """
            import re
            if not re.fullmatch('\d{1,2}:\d{2}', string):
                raise FormatoInvalido("El formato de hora debe ser de 24 horas y de la forma 00:00")
            split_hora = string.split(":")
            hora = int(split_hora[0])
            minutos = int(split_hora[1])
            if hora >= 24 or minutos > 59:
                raise FormatoInvalido("Hora invalida")
            return hora, minutos

    class HorarioInvalido(Exception):
        """ Clase para implementar excepciones cuando la hora de inicio es mayor o igual que la final.
        """
        pass

    def __init__(self, hora_inicial, hora_final):
        """ Constructor de la clase Horario. la hora inicial debe ser menor a la hora final.

        Args:
          hora_inicial: una cadena de texto con la hora inicial.
          hora_final: una cadena de texto con la hora final.
        """
        inicial = self.Hora(hora_inicial)
        final = self.Hora(hora_final)	
        try:
            self._verifica_horario(inicial, final)
        except HorarioInvalido as e:
            sys.exit(e)

        self.hora_inicial = str(inicial)
        self.hora_final = str(final)

    def __str__(self):
        """ Regresa una representacion en cadena del Horario.

        Returns: Una representación en cadena del objeto Horario.
        """
        return "{}, de las {} horas a las {} horas".format(self.dia, self.hora_inicial, self.hora_final) 

    def _verifica_horario(self, inicial, final):
        """ Método auxiliar para validar que la hora inicial sea menor a la hora final.

        Args:
          inicial: un objeto Hora con la hora inicial.
          final: un objeto Hora con la hora final.

        Raises:
          HorarioInvalido: si la hora inicial no es menor a la hora final.
        """
        if final <= inicial:
            raise HorarioInvalido("La hora final no puede ser menor o igual que la inicial")

class Cdia(Base):
	""" Catálogo para almacenar los dias de la semana
	"""

	" El nombre de la tabla en el ORM."
	__tablename__ = 'cdia'
	" El id del dìa. La columna es llave primaria y autoincrementable."
	id_dia = Column(Integer, Sequence('id_dia_sequence'), primary_key=True)
	" El dia de la semana. La columna no admite valores repetidos ni nulos."
	dia = Column(String, nullable=False, unique=True)
	" Relación para vincular las tablas Horario y Cdia."
	horarios = relationship('Horario', back_populates='dia')

	def __init__(self, dia):
		""" Constructor de la clase Cdia.

		Args:
		  dia: cadena con el dia de la semana.
		"""
		self.dia = dia

	def __str__(self):
		""" Regresa una representacion en cadena del día.

		Returns: Una representación en cadena del dia.
		"""
		return self.dia

# Creamos el motor de la base, en este caso en SQLite.
engine = create_engine('sqlite:///:memory:')
# Vinculamos los metadatos de la base con el motor.
Base.metadata.create_all(engine)
# Creamos un objeto Session.
Session = sessionmaker(bind=engine)
# Creamos la sesión.
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
	""" Esta función devuelve en formato JSON los alumnos inscritos a cada curso.

	Returns:
	  s: un JSON con los alumnos inscritos a cada curso.
	"""      
	s = "{\n"
	cursos = session.query(Curso).all()
	for n, curso in enumerate(cursos):		
		s += "\t\"{}\": [".format(str(curso))
		alumnos = session.query(Alumno).where(Alumno.curso==curso).all()
		for m, alumno in enumerate(alumnos):
			s += "\"{}\"".format(str(alumno))
			if m != len(alumnos) - 1:
				s += ", "
			else:
				s += "]"
				if n != len(cursos) - 1:
					s += ","
				s+= "\n"
	s += "}\n"		
	return s

def exportaHorarioProfesores():
	""" Esta función devuelve en formato JSON el horario de cada profesor.

	Returns:
	  s: un JSON con el horario de cada profesor.
	"""      
	s = "{\n"
	profesores = session.query(Profesor).all()
	for n, profesor in enumerate(profesores):		
		s += "\t\"{}\": [".format(str(profesor))
		for m, horario in enumerate(profesor.cursos):
			s += "\"{}\"".format(str(horario))
			if m != len(profesor.cursos) - 1:
				s += ", "
			else:
				s += "]"
				if n != len(profesores) - 1:
					s += ","
				s+= "\n"
	s += "}\n"		
	return s

def exportaHorarioCurso():
	""" Esta función devuelve en formato JSON el horario de cada curso.

	Returns:
	  s: un JSON con el horario de cada curso.
	"""      
	s = "{\n"
	cursos = session.query(Curso).all()
	for n, curso in enumerate(cursos):		
		s += "\t\"{}\": [".format(str(curso))
		horarios = session.query(Horario).where(Horario.curso == curso).all()
		for m, horario in enumerate(horarios):
			s += "\"{}\"".format(str(horario))
			if m != len(horarios) - 1:
				s += ", "
			else:
				s += "]"
				if n != len(cursos) - 1:
					s += ","
				s+= "\n"
	s += "}\n"		
	return s

# Los alumnos que pertenecen a los cursos.
print(exportaInscritos())
# El horario de cada profesor.
print(exportaHorarioProfesores())
# El horario de cad curso.
print(exportaHorarioCurso())

# Cerramos la sesion.
session.close()
