from django.db import transaction
from django.utils import timezone
from .models import Prestamo, Multa
from catalog.models import Libro
from django.shortcuts import redirect

def redireccion_por_rol(request):
    if request.user.is_superuser:
        return redirect('/admin/') 
    elif request.user.is_staff:
        return redirect('gestion_prestamos') 
    else:
        return redirect('list_libros') 


def solicitar_prestamo(libro_id, usuario_id, fecha_limite):
    with transaction.atomic():
        libro = Libro.objects.select_for_update().get(id=libro_id)
        if not libro.validacion:
            return None
        return Prestamo.objects.create(libro=libro, usuario_id=usuario_id, fecha_limite=fecha_limite)

def aprobar_prestamo_staff(prestamo_id, staff_user):
    with transaction.atomic():
        p = Prestamo.objects.select_for_update().get(id=prestamo_id)
        p.libro.validacion = False
        p.libro.save()
        p.estado, p.staff_responsable = 'A', staff_user
        p.save()

def solicitar_devolucion_usuario(prestamo_id):
    """
    El usuario avisa que entregó el libro. El estado cambia pero no se libera el libro.
    """
    prestamo = Prestamo.objects.get(id=prestamo_id)
    if prestamo.estado == 'A':
        prestamo.estado = 'D' 
        prestamo.save()

def confirmar_recepcion_staff(prestamo_id, staff_user):
    with transaction.atomic():
        prestamo = Prestamo.objects.select_for_update().get(id=prestamo_id)
        
  
        if prestamo.estado == 'F':
            return

        hoy = timezone.now().date()
        prestamo.fecha_entrega = hoy
        prestamo.estado = 'F' 
        prestamo.staff_responsable = staff_user
        
        prestamo.libro.validacion = True
        prestamo.libro.save()

        if hoy > prestamo.fecha_limite:
            dias = (hoy - prestamo.fecha_limite).days
            monto_calculado = dias * 1000
            

            Multa.objects.update_or_create(
                prestamo=prestamo,
                defaults={
                    'dias_sobrecargo': dias,
                    'monto': monto_calculado
                }
            )
        
        prestamo.save()

