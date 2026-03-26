from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from datetime import datetime
from .models import Prestamo
from .forms import RegistroForm, LoanForm
from .services import solicitar_prestamo, solicitar_devolucion_usuario


def registro_usuario(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('redireccion_home')
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False 
            user.is_superuser = False
            user.save()
            if not request.user.is_superuser:
                login(request, user)
                messages.success(request, f"¡Bienvenido {user.first_name}!")
                return redirect("redireccion_home")
            else:
                messages.success(request, f"Usuario {user.username} creado.")
                return redirect("admin:auth_user_changelist")
    else:
        form = RegistroForm()
    return render(request, "auth/registro.html", {"form": form})

@login_required
def redireccion_por_rol(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.is_staff:
        return redirect('gestion_prestamos')
    return redirect('list_libros')


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.filter(usuario=request.user).order_by('-fecha_inicial')
    return render(request, 'mis_prestamos.html', {'prestamos': prestamos})

@login_required
def crear_prestamo(request, libro_id):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha_limite')
        if not fecha_str:
            messages.error(request, "Debes seleccionar una fecha.")
            return render(request, 'prestamo_form.html', {'libro_id': libro_id})
        
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        solicitar_prestamo(libro_id, request.user.id, fecha_dt)
        messages.success(request, "Solicitud enviada al Staff.")
        return redirect('mis_prestamos')
    return render(request, 'prestamo_form.html', {'libro_id': libro_id})

@login_required
def vista_devolver_libro(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk, usuario=request.user)
    if prestamo.estado == 'A':
        solicitar_devolucion_usuario(prestamo.pk)
        messages.warning(request, "Aviso de entrega enviado al Staff.")
    return redirect('mis_prestamos')


@login_required
def gestion_total_prestamos(request):
    if not request.user.is_staff:
        return redirect('list_libros')
    prestamos = Prestamo.objects.all().order_by('-fecha_inicial')
    return render(request, 'loans/gestion_total.html', {'prestamos': prestamos})

@login_required
def aprobar_prestamo(request, pk):
    if not request.user.is_staff:
        return redirect('list_libros')
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if prestamo.estado == 'P':
        prestamo.estado = 'A'
        prestamo.save()
        messages.success(request, "Préstamo aprobado con éxito.")
    return redirect('gestion_prestamos')

@login_required
def devolver_libro_staff(request, pk):
    if not request.user.is_staff:
        return redirect('list_libros')
    prestamo = get_object_or_404(Prestamo, pk=pk)
    prestamo.estado = 'F' 
    prestamo.activo = False
    prestamo.save()
    
    libro = prestamo.libro
    libro.validacion = True 
    libro.save()
    
    messages.success(request, f"Recepción confirmada. '{libro.titulo}' disponible.")
    return redirect('gestion_prestamos')

@login_required
def crear_prestamo_manual(request):
    if not request.user.is_staff:
        return redirect('list_libros')
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():

            prestamo = form.save(commit=False)
            prestamo.activo = True
            prestamo.estado = 'A'
            prestamo.save()
            
            libro = prestamo.libro
            libro.validacion = False
            libro.save()
            
            messages.success(request, "Préstamo manual creado y libro bloqueado.")
            return redirect('gestion_prestamos')
    else:
        form = LoanForm()

    return render(request, 'prestamo_form.html', {'form': form })

