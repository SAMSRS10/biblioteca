from django.db import models

# Create your models here.
class Autor(models.Model):
    nombre= models.CharField(max_length=150)
    
    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo= models.CharField(max_length=150)
    isbn= models.CharField(max_length=13, unique=True)
    validacion= models.BooleanField(default=True)
    autor=models.ForeignKey(Autor, on_delete=models.CASCADE)
    
    class Meta: 
         ordering= ['titulo']
        
    def __str__(self):
        return f"{self.titulo} {self.autor}"
        
    