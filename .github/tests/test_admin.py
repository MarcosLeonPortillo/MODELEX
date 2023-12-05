from django.contrib.admin.sites import site
from django.contrib.admin.options import ModelAdmin
from ptpud04.models import Usuario, MotoElectrica, Alquiler

def test_usuario_model_registered():
    assert isinstance(site._registry[Usuario], ModelAdmin)

def test_moto_model_registered():
    assert isinstance(site._registry[MotoElectrica], ModelAdmin)

def test_alquiler_model_registered():
    assert isinstance(site._registry[Alquiler], ModelAdmin)