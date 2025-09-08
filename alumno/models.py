from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from carrera.models import Carrera
from usuario.models import Usuario


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
