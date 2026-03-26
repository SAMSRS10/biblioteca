from django.db import models
from django.contrib.auth.models import User
from catalog.models import Libro
from datetime import date
# Create your models here.
class Prestamo(models.Model):
    ESTADOS = [
        ('P', 'Pendiente de Aprobación'),
        ('A', 'Activo / Entregado'),
        ('D', 'Esperando Recepción Staff'),
        ('F', 'Finalizado / Devuelto'),
    ]
    
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prestamos_usuario')
    staff_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gestiones_staff')
    
    fecha_inicial = models.DateField(auto_now_add=True)
    fecha_limite = models.DateField()
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    activo = models.BooleanField(default=False)

    @property
    def multa_acumulada(self):
        if (self.activo or self.estado == 'D') and date.today() > self.fecha_limite:
            dias = (date.today() - self.fecha_limite).days
            return dias * 1000
        return 0

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username} [{self.get_estado_display()}]"


class Multa(models.Model):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.PROTECT)
    dias_sobrecargo = models.IntegerField(default=0)
    monto= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Multa: {self.prestamo.libro.titulo}"
