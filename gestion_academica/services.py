"""
Servicios para la lógica de negocio del sistema académico.
Implementa la separación de capas y abstracción de la lógica.
"""

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import Usuario, Carrera, Materia, Alumno, Inscripcion


class UsuarioService:
    """
    Servicio para gestionar la lógica de negocio de usuarios
    """
    
    @staticmethod
    def crear_usuario(email, dni, nombre, apellido, grupos=None, password=None):
        """
        Crea un nuevo usuario con validaciones de negocio
        """
        try:
            with transaction.atomic():
                # Validar que no exista el DNI o email
                if Usuario.objects.filter(username=dni).exists():
                    raise ValidationError(f'Ya existe un usuario con DNI {dni}')
                
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError(f'Ya existe un usuario con email {email}')
                
                # Crear usuario
                usuario = Usuario.objects.create_user(
                    email=email,
                    username=dni,
                    first_name=nombre,
                    last_name=apellido,
                    password=password or dni  # Contraseña inicial es el DNI
                )
                
                # Asignar grupos si se proporcionan
                if grupos:
                    usuario.groups.set(grupos)
                
                return usuario
                
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def cambiar_password_primer_login(usuario, nueva_password):
        """
        Cambia la contraseña en el primer login
        """
        if not usuario.primer_login:
            raise ValidationError('El usuario ya cambió su contraseña inicial')
        
        usuario.set_password(nueva_password)
        usuario.primer_login = False
        usuario.save()
        return usuario
    
    @staticmethod
    def autenticar_usuario(email, password):
        """
        Autentica un usuario por email y contraseña
        """
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_password(password):
                return usuario
            return None
        except Usuario.DoesNotExist:
            return None


class CarreraService:
    """
    Servicio para gestionar la lógica de negocio de carreras
    """
    
    @staticmethod
    def crear_carrera(nombre, codigo, descripcion, duracion_años):
        """
        Crea una nueva carrera con validaciones
        """
        try:
            with transaction.atomic():
                # Validar unicidad
                if Carrera.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError(f'Ya existe una carrera con el nombre "{nombre}"')
                
                if Carrera.objects.filter(codigo__iexact=codigo).exists():
                    raise ValidationError(f'Ya existe una carrera con el código "{codigo}"')
                
                carrera = Carrera.objects.create(
                    nombre=nombre.strip().title(),
                    codigo=codigo.upper(),
                    descripcion=descripcion,
                    duracion_años=duracion_años
                )
                
                return carrera
                
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def eliminar_carrera(carrera_id):
        """
        Elimina una carrera validando que no tenga relaciones
        """
        try:
            carrera = Carrera.objects.get(id=carrera_id)
            
            # Validar que no tenga materias ni alumnos
            if carrera.materias.exists():
                raise ValidationError('No se puede eliminar una carrera que tiene materias asociadas')
            
            if carrera.alumnos.exists():
                raise ValidationError('No se puede eliminar una carrera que tiene alumnos asociados')
            
            carrera.delete()
            return True
            
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera no existe')


class MateriaService:
    """
    Servicio para gestionar la lógica de negocio de materias
    """
    
    @staticmethod
    def crear_materia(nombre, codigo, carrera_id, año, cuatrimestre, cupo_maximo, descripcion=""):
        """
        Crea una nueva materia con validaciones
        """
        try:
            with transaction.atomic():
                carrera = Carrera.objects.get(id=carrera_id)
                
                # Validar que no exista la combinación carrera-código
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exists():
                    raise ValidationError(f'Ya existe una materia con código "{codigo}" en esta carrera')
                
                # Validar que el año no supere la duración de la carrera
                if año > carrera.duracion_años:
                    raise ValidationError(f'El año {año} supera la duración de la carrera ({carrera.duracion_años} años)')
                
                materia = Materia.objects.create(
                    nombre=nombre.strip().title(),
                    codigo=codigo.upper(),
                    carrera=carrera,
                    año=año,
                    cuatrimestre=cuatrimestre,
                    cupo_maximo=cupo_maximo,
                    descripcion=descripcion
                )
                
                return materia
                
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def eliminar_materia(materia_id):
        """
        Elimina una materia validando que no tenga inscripciones activas
        """
        try:
            materia = Materia.objects.get(id=materia_id)
            
            # Validar que no tenga inscripciones activas
            if materia.inscripciones.filter(activa=True).exists():
                raise ValidationError('No se puede eliminar una materia que tiene inscripciones activas')
            
            materia.delete()
            return True
            
        except Materia.DoesNotExist:
            raise ValidationError('La materia no existe')
    
    @staticmethod
    def obtener_materias_por_carrera(carrera_id):
        """
        Obtiene todas las materias de una carrera específica
        """
        try:
            carrera = Carrera.objects.get(id=carrera_id)
            return Materia.objects.filter(carrera=carrera, activa=True).order_by('año', 'cuatrimestre', 'nombre')
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')
    
    @staticmethod
    def obtener_materias_con_cupo():
        """
        Obtiene todas las materias que tienen cupo disponible
        """
        materias_con_cupo = []
        for materia in Materia.objects.filter(activa=True):
            if materia.tiene_cupo:
                materias_con_cupo.append(materia)
        return materias_con_cupo


class AlumnoService:
    """
    Servicio para gestionar la lógica de negocio de alumnos usando composición
    """
    
    @staticmethod
    def crear_alumno(dni, nombre, apellido, email, legajo, carrera_id, año_ingreso):
        """
        Crea un nuevo alumno con validaciones usando composición
        """
        try:
            # Validaciones previas
            if Usuario.objects.filter(username=dni).exists():
                raise ValidationError(f'Ya existe un usuario con DNI {dni}')
            
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError(f'Ya existe un usuario con email {email}')
            
            if Alumno.objects.filter(legajo=legajo).exists():
                raise ValidationError(f'Ya existe un alumno con legajo {legajo}')
            
            carrera = Carrera.objects.get(id=carrera_id)
            
            # Usar el método de clase para crear automáticamente
            alumno = Alumno.crear_con_usuario(
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                email=email,
                legajo=legajo,
                carrera=carrera,
                año_ingreso=año_ingreso
            )
            
            return alumno
                
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')
        except Group.DoesNotExist:
            raise ValidationError('El grupo "Alumnos" no existe. Ejecute el comando crear_grupos')
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def obtener_alumnos_por_carrera(carrera_id):
        """
        Obtiene todos los alumnos de una carrera específica
        """
        try:
            carrera = Carrera.objects.get(id=carrera_id)
            return Alumno.objects.filter(carrera=carrera, activo=True).order_by('usuario__last_name', 'usuario__first_name')
        except Carrera.DoesNotExist:
            raise ValidationError('La carrera especificada no existe')


class InscripcionService:
    """
    Servicio para gestionar la lógica de negocio de inscripciones
    """
    
    @staticmethod
    def inscribir_alumno(alumno_id, materia_id):
        """
        Inscribe un alumno a una materia con todas las validaciones
        """
        try:
            with transaction.atomic():
                alumno = Alumno.objects.get(id=alumno_id)
                materia = Materia.objects.get(id=materia_id)
                
                # Validar que la materia pertenezca a la carrera del alumno
                if alumno.carrera != materia.carrera:
                    raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera')
                
                # Validar que no esté ya inscripto
                if Inscripcion.objects.filter(alumno=alumno, materia=materia).exists():
                    raise ValidationError('El alumno ya está inscripto en esta materia')
                
                # Validar cupo disponible
                if not materia.tiene_cupo:
                    raise ValidationError('No hay cupo disponible en esta materia')
                
                # Crear inscripción
                inscripcion = Inscripcion.objects.create(
                    alumno=alumno,
                    materia=materia,
                    activa=True
                )
                
                return inscripcion
                
        except (Alumno.DoesNotExist, Materia.DoesNotExist):
            raise ValidationError('El alumno o la materia especificados no existen')
        except IntegrityError as e:
            raise ValidationError(f'Error de integridad: {str(e)}')
    
    @staticmethod
    def dar_de_baja_inscripcion(inscripcion_id):
        """
        Da de baja una inscripción
        """
        try:
            inscripcion = Inscripcion.objects.get(id=inscripcion_id, activa=True)
            inscripcion.dar_de_baja()
            return inscripcion
        except Inscripcion.DoesNotExist:
            raise ValidationError('La inscripción no existe o ya está dada de baja')
    
    @staticmethod
    def obtener_inscripciones_alumno(alumno_id):
        """
        Obtiene todas las inscripciones activas de un alumno
        """
        try:
            alumno = Alumno.objects.get(id=alumno_id)
            return Inscripcion.objects.filter(alumno=alumno, activa=True).select_related('materia')
        except Alumno.DoesNotExist:
            raise ValidationError('El alumno especificado no existe')
    
    @staticmethod
    def obtener_alumnos_materia(materia_id):
        """
        Obtiene todos los alumnos inscritos en una materia
        """
        try:
            materia = Materia.objects.get(id=materia_id)
            return Inscripcion.objects.filter(materia=materia, activa=True).select_related('alumno')
        except Materia.DoesNotExist:
            raise ValidationError('La materia especificada no existe')


class ReportesService:
    """
    Servicio para generar reportes y consultas específicas
    """
    
    @staticmethod
    def reporte_general():
        """
        Genera un reporte general del sistema
        """
        return {
            'total_carreras': Carrera.objects.filter(activa=True).count(),
            'total_materias': Materia.objects.filter(activa=True).count(),
            'total_alumnos': Alumno.objects.filter(activo=True).count(),
            'total_inscripciones': Inscripcion.objects.filter(activa=True).count(),
            'total_usuarios': Usuario.objects.filter(is_active=True).count(),
        }
    
    @staticmethod
    def materias_con_cupo_por_carrera():
        """
        Retorna materias con cupo agrupadas por carrera
        """
        resultado = {}
        for carrera in Carrera.objects.filter(activa=True):
            materias_con_cupo = []
            for materia in carrera.materias.filter(activa=True):
                if materia.tiene_cupo:
                    materias_con_cupo.append(materia)
            resultado[carrera] = materias_con_cupo
        return resultado
