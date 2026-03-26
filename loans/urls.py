from django.urls import path
from . import views

urlpatterns = [

    path('panel-control/', views.gestion_total_prestamos, name='gestion_prestamos'),
    path('nuevo-manual/', views.crear_prestamo_manual, name='crear_prestamo_manual'),
    path('aprobar/<int:pk>/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('confirmar-recepcion/<int:pk>/', views.devolver_libro_staff, name='devolver_libro_staff'),


    path('redireccionar/', views.redireccion_por_rol, name='redireccion_home'),
    path('registro/', views.registro_usuario, name='registro'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('avisar-entrega/<int:pk>/', views.vista_devolver_libro, name='devolver_libro'),
    path('solicitar/<int:libro_id>/', views.crear_prestamo, name='crear_prestamo'),
]


