from django.contrib import admin

# Register your models here.
from .models import Inscripcion, Alumno, Materia

admin.site.register(Inscripcion)
admin.site.register(Alumno)
admin.site.register(Materia)