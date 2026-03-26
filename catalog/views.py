from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Libro
from loans.models import Prestamo
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def list_libros(request):
    query = request.GET.get('q', '')

    libros_list = Libro.objects.select_related('autor').all()

    if query:
        libros_list = libros_list.filter(
            Q(titulo__icontains=query) | Q(autor__nombre__icontains=query)
        )
    
    paginator = Paginator(libros_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/list_libros.html', {
        'page_obj': page_obj,
        'query': query
    })

def detalle_libro(request, pk):
    libro_obj = get_object_or_404(Libro, pk=pk)
    ultimo_p = Prestamo.objects.filter(libro=libro_obj).order_by('-fecha_inicial').first()
    return render(request, 'catalog/detalle_libro.html', {
        'libro': libro_obj, 
        'ultimo': ultimo_p
    })

class LibroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'autor', 'isbn', 'validacion']
    template_name = 'catalog/libro_form.html'
    success_url = reverse_lazy('list_libros')
    
    def test_func(self):
        return self.request.user.is_staff 

class LibroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Libro
    template_name = 'catalog/libro_confirm_delete.html'
    success_url = reverse_lazy('list_libros')

    def test_func(self):
        return self.request.user.is_staff
