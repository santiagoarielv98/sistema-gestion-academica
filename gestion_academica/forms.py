"""
Formularios para el sistema de gestión académica.
Implementa validaciones y reutilización de código.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Usuario, Carrera, Materia, Alumno, Inscripcion
from .services import UsuarioService


class LoginForm(AuthenticationForm):
    """
    Formulario personalizado de login usando email en lugar de username
    """
    username = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'required': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'required': True
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Intentar autenticar por email
            try:
                usuario = Usuario.objects.get(email=email)
                if usuario.check_password(password):
                    if not usuario.is_active:
                        raise ValidationError('Esta cuenta está desactivada.')
                    self.user_cache = usuario
                else:
                    raise ValidationError('Email o contraseña incorrectos.')
            except Usuario.DoesNotExist:
                raise ValidationError('Email o contraseña incorrectos.')

        return self.cleaned_data


class CambiarPasswordForm(forms.Form):
    """
    Formulario para cambiar contraseña en el primer login
    """
    password_actual = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'})
    )
    nueva_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
        min_length=8,
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    confirmar_password = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar nueva contraseña'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise ValidationError('La contraseña actual es incorrecta.')
        return password_actual

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if nueva_password and confirmar_password:
            if nueva_password != confirmar_password:
                raise ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def save(self):
        nueva_password = self.cleaned_data['nueva_password']
        return UsuarioService.cambiar_password_primer_login(self.user, nueva_password)


class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear y editar usuarios
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(),
        required=False,
        help_text='Dejar vacío para usar DNI como contraseña inicial'
    )

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'first_name', 'last_name', 'rol', 'password']
        labels = {
            'email': 'Correo Electrónico',
            'username': 'DNI',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rol': 'Rol',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'dni': forms.TextInput(attrs={'placeholder': '12345678', 'maxlength': '8'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            # Validar que solo contenga dígitos y tenga 8 caracteres
            if not dni.isdigit() or len(dni) != 8:
                raise ValidationError('El DNI debe tener exactamente 8 dígitos.')
            
            # Validar unicidad (excepto si estamos editando el mismo usuario)
            if self.instance.pk:
                if Usuario.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
            else:
                if Usuario.objects.filter(dni=dni).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
        
        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validar unicidad (excepto si estamos editando el mismo usuario)
            if self.instance.pk:
                if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
            else:
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
        
        return email.lower()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Si no se proporciona contraseña, usar el DNI
        if not password:
            password = self.cleaned_data['dni']
        
        if not usuario.pk:  # Usuario nuevo
            usuario.set_password(password)
        elif password:  # Usuario existente con nueva contraseña
            usuario.set_password(password)
            usuario.primer_login = True
        
        if commit:
            usuario.save()
        
        return usuario


class CarreraForm(forms.ModelForm):
    """
    Formulario para crear y editar carreras
    """
    class Meta:
        model = Carrera
        fields = ['nombre', 'codigo', 'descripcion', 'duracion_años']
        labels = {
            'nombre': 'Nombre de la Carrera',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'duracion_años': 'Duración en Años',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Técnico en Programación'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej: TP2024', 'style': 'text-transform: uppercase;'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la carrera...'}),
            'duracion_años': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            # Validar unicidad (excepto si estamos editando la misma carrera)
            if self.instance.pk:
                if Carrera.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una carrera con este nombre.')
            else:
                if Carrera.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError('Ya existe una carrera con este nombre.')
        
        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper().strip()
            # Validar unicidad (excepto si estamos editando la misma carrera)
            if self.instance.pk:
                if Carrera.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una carrera con este código.')
            else:
                if Carrera.objects.filter(codigo__iexact=codigo).exists():
                    raise ValidationError('Ya existe una carrera con este código.')
        
        return codigo


class MateriaForm(forms.ModelForm):
    """
    Formulario para crear y editar materias
    """
    class Meta:
        model = Materia
        fields = ['nombre', 'codigo', 'carrera', 'año', 'cuatrimestre', 'cupo_maximo', 'descripcion']
        labels = {
            'nombre': 'Nombre de la Materia',
            'codigo': 'Código',
            'carrera': 'Carrera',
            'año': 'Año',
            'cuatrimestre': 'Cuatrimestre',
            'cupo_maximo': 'Cupo Máximo',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Programación I'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej: PROG101', 'style': 'text-transform: uppercase;'}),
            'año': forms.NumberInput(attrs={'min': '1', 'max': '6'}),
            'cupo_maximo': forms.NumberInput(attrs={'min': '1', 'max': '100', 'value': '30'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la materia...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo carreras activas
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)

    def clean(self):
        cleaned_data = super().clean()
        carrera = cleaned_data.get('carrera')
        codigo = cleaned_data.get('codigo')
        año = cleaned_data.get('año')

        # Validar que el código no se repita en la misma carrera
        if carrera and codigo:
            codigo = codigo.upper().strip()
            if self.instance.pk:
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe una materia con este código en la carrera seleccionada.')
            else:
                if Materia.objects.filter(carrera=carrera, codigo__iexact=codigo).exists():
                    raise ValidationError('Ya existe una materia con este código en la carrera seleccionada.')

        # Validar que el año no supere la duración de la carrera
        if carrera and año:
            if año > carrera.duracion_años:
                raise ValidationError(f'El año {año} supera la duración de la carrera ({carrera.duracion_años} años).')

        return cleaned_data

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper().strip()
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
        return nombre


class AlumnoForm(forms.ModelForm):
    """
    Formulario para crear y editar alumnos
    """
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 
                 'legajo', 'carrera', 'año_ingreso']
        labels = {
            'username': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'legajo': 'Legajo',
            'carrera': 'Carrera',
            'año_ingreso': 'Año de Ingreso',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '12345678', 'maxlength': '8'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+54 11 1234-5678'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'legajo': forms.TextInput(attrs={'placeholder': '2024001'}),
            'año_ingreso': forms.NumberInput(attrs={'min': '2000', 'max': '2030'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo carreras activas
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            # Validar que solo contenga dígitos y tenga 8 caracteres
            if not dni.isdigit() or len(dni) != 8:
                raise ValidationError('El DNI debe tener exactamente 8 dígitos.')
            
            # Validar unicidad (excepto si estamos editando el mismo alumno)
            if self.instance.pk:
                if Alumno.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un alumno con este DNI.')
            else:
                if Alumno.objects.filter(dni=dni).exists():
                    raise ValidationError('Ya existe un alumno con este DNI.')
        
        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            # Validar unicidad (excepto si estamos editando el mismo alumno)
            if self.instance.pk:
                if Alumno.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un alumno con este email.')
            else:
                if Alumno.objects.filter(email=email).exists():
                    raise ValidationError('Ya existe un alumno con este email.')
        
        return email

    def clean_legajo(self):
        legajo = self.cleaned_data.get('legajo')
        if legajo:
            # Validar unicidad (excepto si estamos editando el mismo alumno)
            if self.instance.pk:
                if Alumno.objects.filter(legajo=legajo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Ya existe un alumno con este legajo.')
            else:
                if Alumno.objects.filter(legajo=legajo).exists():
                    raise ValidationError('Ya existe un alumno con este legajo.')
        
        return legajo

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip().title()
        return apellido


class InscripcionForm(forms.ModelForm):
    """
    Formulario para gestionar inscripciones
    """
    class Meta:
        model = Inscripcion
        fields = ['alumno', 'materia', 'observaciones']
        labels = {
            'alumno': 'Alumno',
            'materia': 'Materia',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones (opcional)...'}),
        }

    def __init__(self, *args, **kwargs):
        carrera_id = kwargs.pop('carrera_id', None)
        super().__init__(*args, **kwargs)
        
        if carrera_id:
            # Filtrar alumnos y materias de la misma carrera
            self.fields['alumno'].queryset = Alumno.objects.filter(carrera_id=carrera_id, activo=True)
            self.fields['materia'].queryset = Materia.objects.filter(carrera_id=carrera_id, activa=True)
        else:
            self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
            self.fields['materia'].queryset = Materia.objects.filter(activa=True)

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get('alumno')
        materia = cleaned_data.get('materia')

        if alumno and materia:
            # Validar que la materia pertenezca a la carrera del alumno
            if alumno.carrera != materia.carrera:
                raise ValidationError('El alumno no puede inscribirse a una materia de otra carrera.')
            
            # Validar que no esté ya inscripto
            if Inscripcion.objects.filter(alumno=alumno, materia=materia).exists():
                raise ValidationError('El alumno ya está inscripto en esta materia.')
            
            # Validar cupo disponible
            if not materia.tiene_cupo:
                raise ValidationError('No hay cupo disponible en esta materia.')

        return cleaned_data


class FiltroMateriaForm(forms.Form):
    """
    Formulario para filtrar materias por carrera
    """
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True),
        empty_label="Todas las carreras",
        required=False,
        label="Filtrar por Carrera"
    )


class FiltroAlumnoMateriaForm(forms.Form):
    """
    Formulario para filtrar alumnos o materias
    """
    alumno = forms.ModelChoiceField(
        queryset=Alumno.objects.filter(activo=True),
        empty_label="Seleccionar alumno",
        required=False,
        label="Ver materias del alumno"
    )
    
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.filter(activa=True),
        empty_label="Seleccionar materia",
        required=False,
        label="Ver alumnos de la materia"
    )
