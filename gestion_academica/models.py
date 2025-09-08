"""
Modelos para el sistema de gestión académica.
Implementa composición y uso de grupos de Django para roles.
"""

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from usuario.models import Usuario


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


class Alumno(models.Model):
    """
    Modelo para alumnos usando composición en lugar de herencia.
    Tiene una relación con Usuario y contiene datos específicos del alumno.
    """
    # Composición: relación con Usuario en lugar de herencia
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil_alumno',
        verbose_name='Usuario'
    )
    
    # Datos específicos del alumno
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
    año_ingreso = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2030)],
        verbose_name='Año de Ingreso'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['usuario__last_name', 'usuario__first_name']

    def __str__(self):
        return f"{self.nombre_completo} (Legajo: {self.legajo})"

    @property
    def nombre_completo(self):
        """Acceso a nombre completo a través de composición"""
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    @property
    def nombre(self):
        """Acceso al nombre a través de composición"""
        return self.usuario.first_name

    @property
    def apellido(self):
        """Acceso al apellido a través de composición"""
        return self.usuario.last_name

    @property
    def email(self):
        """Acceso al email a través de composición"""
        return self.usuario.email

    @property
    def dni(self):
        """Acceso al DNI a través de composición"""
        return self.usuario.username

    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar que el año de ingreso sea lógico
        if self.año_ingreso and self.año_ingreso > 2030:
            raise ValidationError('El año de ingreso no puede ser mayor a 2030')

    @classmethod
    def crear_con_usuario(cls, dni, nombre, apellido, email, legajo, carrera, año_ingreso):
        """
        Método de clase para crear un alumno con su usuario automáticamente
        """
        from django.db import transaction
        
        with transaction.atomic():
            # Crear usuario usando el método de clase
            usuario = Usuario.crear_con_grupo(
                username=dni,
                first_name=nombre,
                last_name=apellido,
                email=email,
                grupo_name='Alumnos',
                password=dni
            )
            
            # Crear alumno
            alumno = cls.objects.create(
                usuario=usuario,
                legajo=legajo,
                carrera=carrera,
                año_ingreso=año_ingreso
            )
            
            return alumno

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
        if not self.pk:  # Nueva inscripción
            self.fecha_inscripcion = timezone.now()
        super().save(*args, **kwargs)

    def dar_de_baja(self):
        """Método para dar de baja la inscripción"""
        self.activa = False
        self.save()


# SIGNALS para automatizar la creación de usuarios al crear alumnos
@receiver(post_save, sender=Alumno)
def crear_usuario_para_alumno(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta después de crear un alumno.
    Si el alumno no tiene usuario asociado, lo crea automáticamente.
    Solo se ejecuta si el alumno se crea sin usuario (casos edge).
    """
    if created and not instance.usuario:
        # Crear usuario automáticamente usando el método de clase
        usuario = Usuario.crear_con_grupo(
            username=f"temp_{instance.legajo}",  # DNI temporal
            first_name="Pendiente",  # Se actualizará posteriormente
            last_name="Pendiente",  # Se actualizará posteriormente
            email=f"temp_{instance.legajo}@temp.com",  # Email temporal
            grupo_name='Alumnos',
            password=instance.legajo
        )
        
        # Asociar el usuario al alumno
        instance.usuario = usuario
        instance.save()
