import pytest

from django.contrib.auth.models import User
from ptpud04.models import Usuario, MotoElectrica, Alquiler


@pytest.fixture
def user(db):
    return User.objects.create(username="testuser", first_name="Test", last_name="User", password='12345')


@pytest.fixture
def usuario(db, user):
    return Usuario.objects.create(user=user, saldo=100.00)


@pytest.fixture
def moto(db):
    return MotoElectrica.objects.create(
        marca="Test Brand", modelo="Test Model", tarifa_segundo=0.01
    )

@pytest.fixture
def moto_libre(db):
    return MotoElectrica.objects.create(
        marca="Test Brand 2", modelo="Test Model 2", tarifa_segundo=0.0199
    )

@pytest.fixture
def alquiler(db, moto, usuario):
    return Alquiler.objects.create(
        moto=moto, usuario=usuario, inicio="2022-01-01T00:00:00Z", tarifa_segundo=0.01
    )