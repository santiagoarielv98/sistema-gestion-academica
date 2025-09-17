from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import Usuario, Carrera, Alumno



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
