
import datetime
import random
import pytest
from django.urls import reverse
from ptpud04.models import Alquiler, MotoElectrica, Usuario
from django.core.management import call_command
from pytest_django.asserts import assertTemplateUsed

from ptpud04.views import round_up

ALQUILA_VIEW_NAME = "alquila"
LIBERA_VIEW_NAME = "libera"

@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
     with django_db_blocker.unblock():
         call_command('loaddata', 'dump_profesor.json')

def test_alquilar_view_404(db, client, usuario):
    # Generate a pk that is not from a registered MotoElectrica
    client.force_login(usuario.user)
    valid_pk = MotoElectrica.objects.all().last().pk
    invalid_pk = valid_pk + 1
    # Generate the URL for the alquilar view with the invalid pk
    url = reverse(ALQUILA_VIEW_NAME, kwargs={"pk": invalid_pk})
    # Send a GET request to the alquilar view with the invalid pk
    response = client.get(url)
    # Assert that the response status code is 404
    assert response.status_code == 404
    response = client.post(url)
    assert response.status_code == 404
    url = reverse(ALQUILA_VIEW_NAME, kwargs={"pk": valid_pk})
    response = client.get(url)
    assert response.status_code == 200


def test_alquilar_view_requires_login(client, usuario, moto_libre):
    # Try to access the alquilar view without logging in
    response = client.get(reverse(ALQUILA_VIEW_NAME, kwargs={'pk': moto_libre.pk}))
    assert response.status_code == 302  # Should now be able to access the page

    # Now log in and try again
    client.force_login(usuario.user)
    response = client.get(reverse(ALQUILA_VIEW_NAME, kwargs={'pk': moto_libre.pk}))
    assert response.status_code in (200, 404)
        

@pytest.mark.usefixtures("alquiler")
def test_alquilada_flag(db, client, moto, usuario):
    client.force_login(usuario.user)
    url = reverse(ALQUILA_VIEW_NAME, kwargs={"pk": moto.pk})
    # Send a GET request to the alquilar view with the invalid pk
    response = client.get(url)
    assert 'alquilada' in response.context and response.context['alquilada'] == True
    alquiler = Alquiler.objects.get(moto=moto)
    alquiler.fin = datetime.datetime.now()
    alquiler.save() 
    response = client.get(url)
    assert 'alquilada' in response.context and response.context['alquilada'] == False
    alquiler.fin = None
    alquiler.save()
    response = client.get(url)
    assert 'alquilada' in response.context and response.context['alquilada'] == True
    alquiler.delete()
    response = client.get(url)
    assert 'alquilada' in response.context and response.context['alquilada'] == False


def test_cliente_saldo(db, client, moto, usuario):
    
    client.force_login(usuario.user)
    url = reverse(ALQUILA_VIEW_NAME, kwargs={"pk": moto.pk})
    
    check_saldo(client, url, usuario, 9.99, False)
    check_saldo(client, url, usuario, 10, True)
    for i in range(100):
        check_saldo(client, url, usuario, round(random.uniform(0, 9.99), 2), False)
        check_saldo(client, url, usuario, round(random.uniform(10.00, 10000000.00), 2), True)
        
def check_saldo(client, url, usuario, saldo, result):
    usuario.saldo = saldo
    usuario.save() 
    response = client.get(url)
    assert 'saldo_valido' in response.context and response.context['saldo_valido'] == result
    

def test_alquilar_view_post(db, client, usuario, moto_libre):
    client.force_login(usuario.user)
    url = reverse(ALQUILA_VIEW_NAME, kwargs={"pk": moto_libre.pk})
    previous_datetime = datetime.datetime.now()
    assert not Alquiler.objects.filter(moto=moto_libre, fin__isnull=True, tarifa_segundo=moto_libre.tarifa_segundo).exists()
    response = client.post(url)
    assert Alquiler.objects.filter(moto=moto_libre, fin__isnull=True, tarifa_segundo=moto_libre.tarifa_segundo,
                                   inicio__gte=previous_datetime).exists()
    assert response.status_code == 302
    assert response.url == reverse("welcome")
    
"""
Tests de Liberar    
"""
    
def test_liberar_view_moto_404(db, client, usuario):
    # Generate a pk that is not from a registered MotoElectrica
    client.force_login(usuario.user)
    valid_pk = MotoElectrica.objects.all().last().pk
    invalid_pk = valid_pk + 1
    # Generate the URL for the alquilar view with the invalid pk
    url = reverse(LIBERA_VIEW_NAME, kwargs={"pk": invalid_pk})
    # Send a GET request to the alquilar view with the invalid pk
    response = client.get(url)
    # Assert that the response status code is 404
    assert response.status_code == 404
    
    
def test_liberar_view_requires_login(db, client, usuario, moto):
    # Try to access the alquilar view without logging in
    response = client.get(reverse(LIBERA_VIEW_NAME, kwargs={'pk': moto.pk}))
    assert response.status_code == 302

    # Now log in and try again
    client.force_login(usuario.user)
    response = client.get(reverse(LIBERA_VIEW_NAME, kwargs={'pk': moto.pk}))
    assert response.status_code in (200, 404)  # Should now be able to access the page
        
def test_liberar_view_moto_esta_alquilada_404(db, client, usuario, moto_libre):
    # Now log in and try again
    client.force_login(usuario.user)
    response = client.get(reverse(LIBERA_VIEW_NAME, kwargs={'pk': moto_libre.pk}))
    assert response.status_code == 404  # Should now be able to access the page
    
def test_liberar_view_moto_ajena_404(db, client, usuario):
    # Now log in and try again
    client.force_login(usuario.user)
    response = client.get(reverse(LIBERA_VIEW_NAME, kwargs={'pk': 1}))
    assert response.status_code == 404  # Should now be able to access the page
    
def test_liberar_moto(db, client):
    moto = MotoElectrica.objects.get(pk=1)
    usuario = Usuario.objects.get(pk=1)
    alquiler = Alquiler.objects.get(moto=moto, fin__isnull=True, usuario=usuario, coste_total__isnull=True)
    tarifa_segundo = alquiler.tarifa_segundo
    saldo_previo = usuario.saldo
    client.force_login(usuario.user)
    response = client.get(reverse(LIBERA_VIEW_NAME, kwargs={'pk': 1}))
    alquiler.refresh_from_db()
    usuario.refresh_from_db()
    check_libera_template_response(response, alquiler, moto)
    assert alquiler.fin is not None
    assert alquiler.fin >= alquiler.inicio
    assert alquiler.coste_total is not None
    assert float(alquiler.coste_total) == round_up((alquiler.fin - alquiler.inicio).total_seconds() * float(tarifa_segundo))
    assert usuario.saldo == saldo_previo - alquiler.coste_total
    
def check_libera_template_response(response, alquiler, moto):
    assert response.status_code == 200
    # Check the the template used is the correct one
    assertTemplateUsed(response, 'ptpud04/free.html')
    assert response.context['alquiler'] == alquiler
    assert response.context['moto'] == moto