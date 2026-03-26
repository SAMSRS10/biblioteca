from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_libros, name='list_libros'),
    path('libro/<int:pk>/', views.detalle_libro, name='detalle_libro'),

]
