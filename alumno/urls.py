"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/', views.AlumnoListView.as_view(), name='alumno_list'),
    path('alumnos/crear/', views.AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumnos/<int:pk>/', views.AlumnoDetailView.as_view(), name='alumno_detail'),
    path('alumnos/<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumnos/<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno_delete'),
]
