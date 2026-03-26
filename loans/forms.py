from django import forms
from .models import Prestamo
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoanForm(forms.ModelForm):
    class Meta:
        model = Prestamo

        fields = ['libro', 'usuario', 'fecha_limite']
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_libro(self):
        libro_seleccionado = self.cleaned_data.get('libro')
        if libro_seleccionado and libro_seleccionado.validacion == False:
            raise ValidationError("Este libro ya se encuentra prestado actualmente.")
        return libro_seleccionado

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    first_name = forms.CharField(max_length=100, required=True, label="Nombre Completo")

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

