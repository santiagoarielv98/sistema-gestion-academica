from django.contrib import admin

# Register your models here.
from .models import Inscripcion, Alumno, Materia, Carrera

admin.site.register(Inscripcion)
admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Carrera)