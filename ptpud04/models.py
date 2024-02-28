from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Usuario(models.Model):
    """
    En plural el modelo se llama Usuarios
    Su representación como cadena es:
    <nombre_usuario> - <nombre> <apellidos>
    """
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo=models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name_plural = "Usuarios"

class MotoElectrica(models.Model):
    """
    En Singular el modelo se llama 'Moto Electrica'
    En plural el modelo se llama 'Motos Electricas'
    Su representación como cadena es:
    <marca> - <modelo>
    """
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    tarifa_segundo = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        verbose_name = "Moto Electrica"
        verbose_name_plural = "Motos Electricas"

    def __str__(self):
        return f'{self.marca} - {self.modelo}'



class Alquiler(models.Model):
    """
    En plural el modelo se llama Alquileres
    Su representación como cadena es:
    <nombre_usuario> <marca_moto> <fecha_inicio>
    """
    moto = models.ForeignKey(MotoElectrica, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True, null=True)
    tarifa_segundo = models.DecimalField(max_digits=6, decimal_places=4)
    coste_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f'{self.usuario.user.username} {self.moto.marca} {self.inicio}'

    class Meta:
        verbose_name_plural = "Alquileres"