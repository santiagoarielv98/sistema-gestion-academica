"""
URLs para la aplicación de gestión académica
"""

from django.urls import path
from . import views

app_name = 'gestion_academica'

urlpatterns = [
    # Autenticación
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cambiar-password/', views.CambiarPasswordView.as_view(), name='cambiar_password'),
    
    # Página principal
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Gestión de Carreras (solo Admin)
    path('carreras/', views.CarreraListView.as_view(), name='carrera_list'),
    path('carreras/crear/', views.CarreraCreateView.as_view(), name='carrera_create'),
    path('carreras/<int:pk>/editar/', views.CarreraUpdateView.as_view(), name='carrera_update'),
    path('carreras/<int:pk>/eliminar/', views.CarreraDeleteView.as_view(), name='carrera_delete'),
    
    # Gestión de Materias (solo Admin)
    path('materias/', views.MateriaListView.as_view(), name='materia_list'),
    path('materias/crear/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
    
    # Gestión de Alumnos (solo Admin)
    path('alumnos/', views.AlumnoListView.as_view(), name='alumno_list'),
    path('alumnos/crear/', views.AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumnos/<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno_delete'),
    
    # Gestión de Usuarios (solo Admin)
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
    
    # Gestión de Inscripciones
    path('inscripciones/', views.InscripcionListView.as_view(), name='inscripcion_list'),
    path('inscripciones/crear/', views.InscripcionCreateView.as_view(), name='inscripcion_create'),
    path('inscripciones/<int:pk>/dar-baja/', views.InscripcionBajaView.as_view(), name='inscripcion_baja'),
    
    # Vistas específicas para alumnos
    path('mis-materias/', views.MisMateriaView.as_view(), name='mis_materias'),
    path('oferta-academica/', views.OfertaAcademicaView.as_view(), name='oferta_academica'),
    path('inscribirse/<int:materia_id>/', views.InscribirseView.as_view(), name='inscribirse'),
    
    # Vistas para invitados
    path('carreras-publicas/', views.CarrerasPublicasView.as_view(), name='carreras_publicas'),
    path('materias-publicas/', views.MateriasPublicasView.as_view(), name='materias_publicas'),
    
    # Filtros y consultas
    path('materias-por-carrera/', views.MateriasPorCarreraView.as_view(), name='materias_por_carrera'),
    path('alumnos-por-materia/', views.AlumnosPorMateriaView.as_view(), name='alumnos_por_materia'),
    path('materias-con-cupo/', views.MateriasConCupoView.as_view(), name='materias_con_cupo'),
    
    # Reportes
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
]
