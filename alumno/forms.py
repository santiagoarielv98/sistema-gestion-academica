from django import forms
from django.core.exceptions import ValidationError

from materia.models import Materia
from .models import Usuario, Carrera, Alumno

class AlumnoForm(forms.ModelForm):
    """
    Formulario para crear y editar alumnos usando composición
    """
    # Campos del usuario
    dni = forms.CharField(
        max_length=8,
        label='DNI',
        widget=forms.TextInput(attrs={'placeholder': '12345678', 'maxlength': '8'})
    )
    nombre = forms.CharField(
        max_length=100,
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
    )
    apellido = forms.CharField(
        max_length=100,
        label='Apellido',
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'})
    )

    class Meta:
        model = Alumno
        fields = ['legajo', 'carrera', 'año_ingreso']
        labels = {
            'legajo': 'Legajo',
            'carrera': 'Carrera',
            'año_ingreso': 'Año de Ingreso',
        }
        widgets = {
            'legajo': forms.TextInput(attrs={'placeholder': '2024001'}),
            'año_ingreso': forms.NumberInput(attrs={'min': '2000', 'max': '2030'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo carreras activas
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)
        
        # Si estamos editando, cargar datos del usuario relacionado
        if self.instance.pk and hasattr(self.instance, 'usuario'):
            self.fields['dni'].initial = self.instance.usuario.username
            self.fields['nombre'].initial = self.instance.usuario.first_name
            self.fields['apellido'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            # Validar que solo contenga dígitos y tenga 8 caracteres
            if not dni.isdigit() or len(dni) != 8:
                raise ValidationError('El DNI debe tener exactamente 8 dígitos.')
            
            # Validar unicidad en usuarios (excepto si estamos editando el mismo)
            if self.instance.pk and hasattr(self.instance, 'usuario'):
                if Usuario.objects.filter(username=dni).exclude(pk=self.instance.usuario.pk).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
            else:
                if Usuario.objects.filter(username=dni).exists():
                    raise ValidationError('Ya existe un usuario con este DNI.')
        
        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            # Validar unicidad en usuarios (excepto si estamos editando el mismo)
            if self.instance.pk and hasattr(self.instance, 'usuario'):
                if Usuario.objects.filter(email=email).exclude(pk=self.instance.usuario.pk).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
            else:
                if Usuario.objects.filter(email=email).exists():
                    raise ValidationError('Ya existe un usuario con este email.')
        
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

    def save(self, commit=True):
        from django.contrib.auth.models import Group
        
        alumno = super().save(commit=False)
        
        # Crear o actualizar usuario
        if self.instance.pk and hasattr(self.instance, 'usuario'):
            # Editar usuario existente
            usuario = self.instance.usuario
            usuario.username = self.cleaned_data['dni']
            usuario.first_name = self.cleaned_data['nombre']
            usuario.last_name = self.cleaned_data['apellido']
            usuario.email = self.cleaned_data['email']
            usuario.save()
        else:
            # Usar el método de clase para crear alumno con usuario
            if commit:
                return Alumno.crear_con_usuario(
                    dni=self.cleaned_data['dni'],
                    nombre=self.cleaned_data['nombre'],
                    apellido=self.cleaned_data['apellido'],
                    email=self.cleaned_data['email'],
                    legajo=alumno.legajo,
                    carrera=alumno.carrera,
                    año_ingreso=alumno.año_ingreso
                )
        
        if commit:
            alumno.save()
        
        return alumno

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
