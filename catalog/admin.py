from django.contrib import admin
from .models import Autor , Libro 
# Register your models here.

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'validacion')
    search_fields = ('titulo', 'autor__nombre', 'isbn')
    list_filter = ('validacion', 'autor')

