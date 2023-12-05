import pytest

from django.db import models
from django.contrib.auth.models import User
from ptpud04.models import Usuario, MotoElectrica, Alquiler

"""
Tests para Usuario
"""
def test_model_usuario_user_field():
    field = Usuario._meta.get_field('user')
    assert isinstance(field, models.ForeignKey)
    assert field.related_model is User
    assert isrequired(field)

def test_model_usuario_saldo_field():
    field = Usuario._meta.get_field('saldo')
    assert isinstance(field, models.DecimalField)
    assert field.max_digits == 12
    assert field.decimal_places == 2
    assert isrequired(field)

def isrequired(field):
    return field.blank is False and field.null is False

def test_model_usuario_verbose_name_plural():
    assert Usuario._meta.verbose_name_plural == 'Usuarios'


def test_model_usuario_str_representation(usuario, user):
    expected_object_name = f'{user.username} - {user.first_name} {user.last_name}'
    assert str(usuario) == expected_object_name


"""
Tests para MotoElectrica
"""


def test_model_motoelectrica_marca_field():
    field = MotoElectrica._meta.get_field('marca')
    assert isinstance(field, models.CharField)
    assert field.max_length == 50
    assert is_required(field)

def test_model_motoelectrica_modelo_field():
    field = MotoElectrica._meta.get_field('modelo')
    assert isinstance(field, models.CharField)
    assert field.max_length == 50
    assert is_required(field)

def test_model_motoelectrica_tarifa_segundo_field():
    field = MotoElectrica._meta.get_field('tarifa_segundo')
    assert isinstance(field, models.DecimalField)
    assert field.max_digits == 6
    assert field.decimal_places == 4
    assert is_required(field)

def is_required(field):
    return not field.blank and not field.null

def test_model_motoelectrica_verbose_names():
    assert MotoElectrica._meta.verbose_name == 'Moto Electrica'
    assert MotoElectrica._meta.verbose_name_plural == 'Motos Electricas'

def test_model_motoelectrica_str_representation(moto):
    expected_object_name = f'{moto.marca} - {moto.modelo}'
    assert str(moto) == expected_object_name

"""
Tests para Alquiler
"""
def test_model_alquiler_moto_field():
    field = Alquiler._meta.get_field('moto')
    assert isinstance(field, models.ForeignKey)
    assert field.related_model is MotoElectrica
    assert is_required(field)

def test_model_alquiler_usuario_field():
    field = Alquiler._meta.get_field('usuario')
    assert isinstance(field, models.ForeignKey)
    assert field.related_model is Usuario
    assert is_required(field)

def test_model_alquiler_inicio_field():
    field = Alquiler._meta.get_field('inicio')
    assert isinstance(field, models.DateTimeField)
    assert is_required(field)

def test_model_alquiler_fin_field():
    field = Alquiler._meta.get_field('fin')
    assert isinstance(field, models.DateTimeField)
    assert field.blank is True
    assert field.null is True

def test_model_alquiler_tarifa_segundo_field():
    field = Alquiler._meta.get_field('tarifa_segundo')
    assert isinstance(field, models.DecimalField)
    assert field.max_digits == 6
    assert field.decimal_places == 4
    assert is_required(field)

def test_model_alquiler_coste_total_field():
    field = Alquiler._meta.get_field('coste_total')
    assert isinstance(field, models.DecimalField)
    assert field.max_digits == 12
    assert field.decimal_places == 2
    assert field.blank is True
    assert field.null is True

def is_required(field):
    return field.blank is False and field.null is False

def test_model_alquiler_verbose_name_plural():
    assert Alquiler._meta.verbose_name_plural == 'Alquileres'


def test_model_alquiler_str_representation(alquiler):
    expected_object_name = f'{alquiler.usuario.user.username} {alquiler.moto.marca} {alquiler.inicio}'
    assert str(alquiler) == expected_object_name