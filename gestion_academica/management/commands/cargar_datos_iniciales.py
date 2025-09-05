"""
Comando personalizado para cargar datos iniciales de ejemplo
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
from gestion_academica.models import Usuario, Carrera, Materia, Alumno, Inscripcion


class Command(BaseCommand):
    help = 'Carga datos iniciales de ejemplo en el sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de cargar los nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            with transaction.atomic():
                Inscripcion.objects.all().delete()
                Alumno.objects.all().delete()
                Materia.objects.all().delete()
                Carrera.objects.all().delete()
                Usuario.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando datos iniciales...')
        
        try:
            with transaction.atomic():
                # Crear usuarios administradores adicionales
                admin_user, created = Usuario.objects.get_or_create(
                    email='admin@crui.edu.ar',
                    defaults={
                        'dni': '12345678',
                        'first_name': 'Administrador',
                        'last_name': 'Sistema',
                        'rol': 'administrador',
                        'primer_login': False,
                        'is_staff': True,
                        'is_active': True,
                    }
                )
                if created:
                    admin_user.set_password('admin123')
                    admin_user.save()
                    self.stdout.write(f'✓ Usuario administrador creado: {admin_user.email}')

                # Crear usuario invitado
                invitado_user, created = Usuario.objects.get_or_create(
                    email='invitado@ejemplo.com',
                    defaults={
                        'dni': '87654321',
                        'first_name': 'Usuario',
                        'last_name': 'Invitado',
                        'rol': 'invitado',
                        'primer_login': False,
                        'is_active': True,
                    }
                )
                if created:
                    invitado_user.set_password('87654321')
                    invitado_user.save()
                    self.stdout.write(f'✓ Usuario invitado creado: {invitado_user.email}')

                # Crear carreras de ejemplo
                carreras_data = [
                    {
                        'nombre': 'Técnico Superior en Programación',
                        'codigo': 'TSP2024',
                        'descripcion': 'Carrera técnica orientada al desarrollo de software',
                        'duracion_años': 3
                    },
                    {
                        'nombre': 'Técnico Superior en Análisis de Sistemas',
                        'codigo': 'TSAS2024',
                        'descripcion': 'Carrera técnica orientada al análisis y diseño de sistemas',
                        'duracion_años': 3
                    },
                    {
                        'nombre': 'Técnico Superior en Redes y Comunicaciones',
                        'codigo': 'TSRC2024',
                        'descripcion': 'Carrera técnica orientada a redes de datos y comunicaciones',
                        'duracion_años': 2
                    }
                ]

                carreras = {}
                for carrera_data in carreras_data:
                    carrera, created = Carrera.objects.get_or_create(
                        codigo=carrera_data['codigo'],
                        defaults=carrera_data
                    )
                    carreras[carrera_data['codigo']] = carrera
                    if created:
                        self.stdout.write(f'✓ Carrera creada: {carrera.nombre}')

                # Crear materias de ejemplo
                materias_data = [
                    # Técnico en Programación - 1er año
                    {
                        'nombre': 'Fundamentos de Programación',
                        'codigo': 'PROG101',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Matemática Aplicada',
                        'codigo': 'MAT101',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Programación Orientada a Objetos',
                        'codigo': 'POO102',
                        'carrera': 'TSP2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 25
                    },
                    # Técnico en Programación - 2do año
                    {
                        'nombre': 'Bases de Datos',
                        'codigo': 'BD201',
                        'carrera': 'TSP2024',
                        'año': 2,
                        'cuatrimestre': 1,
                        'cupo_maximo': 25
                    },
                    {
                        'nombre': 'Desarrollo Web',
                        'codigo': 'WEB202',
                        'carrera': 'TSP2024',
                        'año': 2,
                        'cuatrimestre': 2,
                        'cupo_maximo': 20
                    },
                    # Análisis de Sistemas
                    {
                        'nombre': 'Análisis y Diseño de Sistemas',
                        'codigo': 'ADS101',
                        'carrera': 'TSAS2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 30
                    },
                    {
                        'nombre': 'Modelado de Procesos',
                        'codigo': 'MP102',
                        'carrera': 'TSAS2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 25
                    },
                    # Redes y Comunicaciones
                    {
                        'nombre': 'Fundamentos de Redes',
                        'codigo': 'RED101',
                        'carrera': 'TSRC2024',
                        'año': 1,
                        'cuatrimestre': 1,
                        'cupo_maximo': 25
                    },
                    {
                        'nombre': 'Configuración de Equipos',
                        'codigo': 'CE102',
                        'carrera': 'TSRC2024',
                        'año': 1,
                        'cuatrimestre': 2,
                        'cupo_maximo': 20
                    }
                ]

                materias = {}
                for materia_data in materias_data:
                    carrera = carreras[materia_data['carrera']]
                    materia_data['carrera'] = carrera
                    del materia_data['carrera']  # Quitar el código, ya tenemos el objeto
                    
                    materia, created = Materia.objects.get_or_create(
                        codigo=materia_data['codigo'],
                        carrera=carrera,
                        defaults=materia_data
                    )
                    materias[materia_data['codigo']] = materia
                    if created:
                        self.stdout.write(f'✓ Materia creada: {materia.nombre}')

                # Crear alumnos de ejemplo
                alumnos_data = [
                    {
                        'dni': '20123456',
                        'nombre': 'Juan Carlos',
                        'apellido': 'González',
                        'email': 'juan.gonzalez@estudiante.crui.edu.ar',
                        'telefono': '+54 11 1234-5678',
                        'fecha_nacimiento': date(2000, 3, 15),
                        'legajo': '2024001',
                        'carrera': 'TSP2024',
                        'año_ingreso': 2024
                    },
                    {
                        'dni': '20234567',
                        'nombre': 'María Elena',
                        'apellido': 'Rodríguez',
                        'email': 'maria.rodriguez@estudiante.crui.edu.ar',
                        'telefono': '+54 11 2345-6789',
                        'fecha_nacimiento': date(1999, 7, 22),
                        'legajo': '2024002',
                        'carrera': 'TSP2024',
                        'año_ingreso': 2024
                    },
                    {
                        'dni': '20345678',
                        'nombre': 'Carlos Alberto',
                        'apellido': 'Fernández',
                        'email': 'carlos.fernandez@estudiante.crui.edu.ar',
                        'telefono': '+54 11 3456-7890',
                        'fecha_nacimiento': date(2001, 1, 10),
                        'legajo': '2024003',
                        'carrera': 'TSAS2024',
                        'año_ingreso': 2024
                    },
                    {
                        'dni': '20456789',
                        'nombre': 'Ana Sofía',
                        'apellido': 'López',
                        'email': 'ana.lopez@estudiante.crui.edu.ar',
                        'telefono': '+54 11 4567-8901',
                        'fecha_nacimiento': date(2000, 11, 5),
                        'legajo': '2024004',
                        'carrera': 'TSRC2024',
                        'año_ingreso': 2024
                    }
                ]

                alumnos = {}
                for alumno_data in alumnos_data:
                    carrera_codigo = alumno_data['carrera']
                    alumno_data['carrera'] = carreras[carrera_codigo]
                    
                    alumno, created = Alumno.objects.get_or_create(
                        dni=alumno_data['dni'],
                        defaults=alumno_data
                    )
                    alumnos[alumno_data['dni']] = alumno
                    if created:
                        self.stdout.write(f'✓ Alumno creado: {alumno.nombre_completo}')

                # Crear algunas inscripciones de ejemplo
                inscripciones_data = [
                    # Juan González (Programación) - 1er año
                    {'alumno': '20123456', 'materia': 'PROG101'},
                    {'alumno': '20123456', 'materia': 'MAT101'},
                    
                    # María Rodríguez (Programación) - 1er año
                    {'alumno': '20234567', 'materia': 'PROG101'},
                    {'alumno': '20234567', 'materia': 'MAT101'},
                    {'alumno': '20234567', 'materia': 'POO102'},
                    
                    # Carlos Fernández (Análisis) - 1er año
                    {'alumno': '20345678', 'materia': 'ADS101'},
                    
                    # Ana López (Redes) - 1er año
                    {'alumno': '20456789', 'materia': 'RED101'},
                ]

                for inscripcion_data in inscripciones_data:
                    alumno = alumnos[inscripcion_data['alumno']]
                    materia = materias[inscripcion_data['materia']]
                    
                    inscripcion, created = Inscripcion.objects.get_or_create(
                        alumno=alumno,
                        materia=materia,
                        defaults={'activa': True}
                    )
                    if created:
                        self.stdout.write(f'✓ Inscripción creada: {alumno.nombre_completo} -> {materia.nombre}')

                self.stdout.write(
                    self.style.SUCCESS('¡Datos iniciales cargados exitosamente!')
                )
                
                # Mostrar resumen
                self.stdout.write('\n--- RESUMEN DE DATOS CARGADOS ---')
                self.stdout.write(f'Carreras: {Carrera.objects.count()}')
                self.stdout.write(f'Materias: {Materia.objects.count()}')
                self.stdout.write(f'Alumnos: {Alumno.objects.count()}')
                self.stdout.write(f'Inscripciones: {Inscripcion.objects.filter(activa=True).count()}')
                self.stdout.write(f'Usuarios: {Usuario.objects.count()}')
                
                self.stdout.write('\n--- USUARIOS DE PRUEBA ---')
                self.stdout.write('Administrador: admin@crui.edu.ar / contraseña: admin123')
                self.stdout.write('Invitado: invitado@ejemplo.com / contraseña: 87654321')
                self.stdout.write('Alumnos: usar email del alumno / contraseña: su DNI')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {str(e)}')
            )
