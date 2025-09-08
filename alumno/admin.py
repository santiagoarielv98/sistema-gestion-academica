from django.contrib import admin

from alumno.models import Alumno

# Register your models here.

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'legajo', 'carrera', 'año_ingreso', 'activo')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'legajo', 'usuario__username')
    list_filter = ('carrera', 'año_ingreso', 'activo')
    ordering = ('usuario__last_name', 'usuario__first_name')

admin.site.register(Alumno, AlumnoAdmin)