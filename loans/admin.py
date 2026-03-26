from django.contrib import admin,messages
from .models import Prestamo, Multa
from .services import aprobar_prestamo_staff, confirmar_recepcion_staff
from django.contrib.admin import ModelAdmin
# Register your models here.

@admin.action(description="1. Aprobar Solicitud (Entregar Libro)")
def action_aprobar_solicitud(modeladmin, request, queryset):
    for p in queryset:
        if p.estado == 'P':
            aprobar_prestamo_staff(p.id, request.user)
    messages.success(request, "Solicitudes aprobadas correctamente.")
@admin.action(description="2. Confirmar Recepción Física (Cerrar)")
def action_confirmar_recepcion(modeladmin, request, queryset):
    for p in queryset:
        if p.estado == 'D':
            confirmar_recepcion_staff(p.id, request.user) 
    messages.success(request, "Libros recibidos correctamente.")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'estado', 'staff_responsable', 'fecha_limite', 'ver_multa')
    list_filter = ('estado', 'activo')
    search_fields = ('usuario__username', 'libro__titulo')
    actions = [action_aprobar_solicitud, action_confirmar_recepcion]

    def ver_multa(self, obj):
        return f"${obj.multa_acumulada}"
    ver_multa.short_description = "Multa Actual"

@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'monto', 'dias_sobrecargo')
    readonly_fields = ('prestamo', 'monto', 'dias_sobrecargo')

