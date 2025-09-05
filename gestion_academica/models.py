"""
Modelos para el sistema de gestión académica.
Implementa herencia, abstracción y encapsulamiento según POO.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Clase abstracta base para aplicar herencia
class Persona(models.Model):
    """
    Clase base abstracta que define los atributos comunes 
    de todas las personas en el sistema.
    Aplica el principio de herencia de POO.
    """
    dni = models.CharField(
        max_length=8, 
        unique=True, 
        validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe tener 8 dígitos')],
        verbose_name='DNI'
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Formato de teléfono inválido')],
        verbose_name='Teléfono'
    )
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')

    class Meta:
        abstract = True  # Clase abstracta - no crea tabla en BD

    def __str__(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"

    @property
    def nombre_completo(self):
        """Propiedad que encapsula la lógica de nombre completo"""
        return f"{self.nombre} {self.apellido}"


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para autenticación.
    Extiende AbstractUser de Django para manejar roles.
    """
    ROLES = [
        ('administrador', 'Administrador'),
        ('alumno', 'Alumno'),
        ('invitado', 'Invitado'),
        ('docente', 'Docente'),
        ('preceptor', 'Preceptor'),
    ]
    
    # Usamos email como username
    username = None
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    dni = models.CharField(
        max_length=8, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe tener 8 dígitos')],
        verbose_name='DNI'
    )
    rol = models.CharField(max_length=20, choices=ROLES, verbose_name='Rol')
    primer_login = models.BooleanField(default=True, verbose_name='Primer Login')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'first_name', 'last_name', 'rol']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para generar contraseña inicial si es nuevo usuario
        """
        if not self.pk and not self.password:
            # Contraseña inicial es el DNI
            self.set_password(self.dni)
        super().save(*args, **kwargs)


class Carrera(models.Model):
    """
    Modelo para las carreras académicas
    """
    nombre = models.CharField(max_length=200, unique=True, verbose_name='Nombre de la Carrera')
    codigo = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(regex=r'^[A-Z]{2,4}\d{2,4}$', message='Formato: AA1234')],
        verbose_name='Código'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    duracion_años = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Duración en Años'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    def clean(self):
        """Validaciones personalizadas"""
        if self.nombre:
            self.nombre = self.nombre.strip().title()

    def delete(self, *args, **kwargs):
        """
        Validación: No permitir eliminar si tiene materias o alumnos
        """
        if self.materias.exists():
            raise ValidationError('No se puede eliminar una carrera que tiene materias asociadas')
        if self.alumnos.exists():
            raise ValidationError('No se puede eliminar una carrera que tiene alumnos asociados')
        super().delete(*args, **kwargs)


class Materia(models.Model):
    """
    Modelo para las materias académicas
    """
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la Materia')
    codigo = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^[A-Z]{2,4}\d{3,4}$', message='Formato: ABC123')],
        verbose_name='Código'
    )
    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.CASCADE, 
        related_name='materias',
        verbose_name='Carrera'
    )
    año = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='Año'
    )
    cuatrimestre = models.PositiveIntegerField(
        choices=[(1, 'Primer Cuatrimestre'), (2, 'Segundo Cuatrimestre')],
        verbose_name='Cuatrimestre'
    )
    cupo_maximo = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Cupo Máximo'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        unique_together = ['carrera', 'codigo']  # No duplicar códigos por carrera
        ordering = ['carrera', 'año', 'cuatrimestre', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.carrera.nombre} ({self.año}° año)"

    def clean(self):
        """Validaciones personalizadas"""
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        
        # Validar que el año no supere la duración de la carrera
        if self.carrera and self.año > self.carrera.duracion_años:
            raise ValidationError(f'El año {self.año} supera la duración de la carrera ({self.carrera.duracion_años} años)')

    @property
    def cupo_disponible(self):
        """Propiedad que calcula el cupo disponible"""
        inscriptos = self.inscripciones.filter(activa=True).count()
        return self.cupo_maximo - inscriptos

    @property
    def tiene_cupo(self):
        """Propiedad que indica si hay cupo disponible"""
        return self.cupo_disponible > 0

    def delete(self, *args, **kwargs):
        """
        Validación: No permitir eliminar si tiene inscripciones activas
        """
        if self.inscripciones.filter(activa=True).exists():
            raise ValidationError('No se puede eliminar una materia que tiene inscripciones activas')
        super().delete(*args, **kwargs)


class Alumno(Persona):
    """
    Modelo para alumnos que hereda de Persona.
    Implementa herencia de POO.
    """
    legajo = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{4,10}$', message='El legajo debe tener entre 4 y 10 dígitos')],
        verbose_name='Legajo'
    )
    carrera = models.ForeignKey(
        Carrera, 
        on_delete=models.CASCADE, 
        related_name='alumnos',
        verbose_name='Carrera'
    )
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='alumno',
        null=True, 
        blank=True,
        verbose_name='Usuario'
    )
    año_ingreso = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2030)],
        verbose_name='Año de Ingreso'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido', 'nombre']

    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        # Si tiene usuario, validar que los datos coincidan
        if self.usuario:
            if self.usuario.dni != self.dni:
                raise ValidationError('El DNI del usuario debe coincidir con el del alumno')
            if self.usuario.email != self.email:
                raise ValidationError('El email del usuario debe coincidir con el del alumno')

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para crear usuario automáticamente si no existe
        """
        super().save(*args, **kwargs)
        
        # Crear usuario si no existe
        if not self.usuario:
            usuario = Usuario.objects.create_user(
                email=self.email,
                dni=self.dni,
                first_name=self.nombre,
                last_name=self.apellido,
                rol='alumno'
            )
            self.usuario = usuario
            super().save(*args, **kwargs)

    @property
    def materias_inscripto(self):
        """Propiedad que retorna las materias en las que está inscripto"""
        return self.inscripciones.filter(activa=True)


class Inscripcion(models.Model):
    """
    Modelo para gestionar las inscripciones de alumnos a materias.
    Tabla intermedia con información adicional.
    """
    alumno = models.ForeignKey(
        Alumno, 
        on_delete=models.CASCADE, 
        related_name='inscripciones',
        verbose_name='Alumno'
    )
    materia = models.ForeignKey(
        Materia, 
        on_delete=models.CASCADE, 
        related_name='inscripciones',
        verbose_name='Materia'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Inscripción')
    fecha_baja = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Baja')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['alumno', 'materia']  # Un alumno no puede inscribirse dos veces a la misma materia
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        estado = "Activa" if self.activa else "Dada de baja"
        return f"{self.alumno.nombre_completo} - {self.materia.nombre} ({estado})"

    def clean(self):
        """Validaciones personalizadas"""
        # Validar que la materia pertenezca a la carrera del alumno
        if self.alumno and self.materia:
            if self.alumno.carrera != self.materia.carrera:
                raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera')
            
            # Validar cupo disponible
            if self.materia.cupo_disponible <= 0 and self.activa:
                raise ValidationError('No hay cupo disponible en esta materia')

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para manejar la lógica de baja
        """
        if not self.activa and self.fecha_baja is None:
            from django.utils import timezone
            self.fecha_baja = timezone.now()
        elif self.activa:
            self.fecha_baja = None
        
        super().save(*args, **kwargs)

    def dar_de_baja(self):
        """Método para dar de baja la inscripción"""
        self.activa = False
        from django.utils import timezone
        self.fecha_baja = timezone.now()
        self.save()
