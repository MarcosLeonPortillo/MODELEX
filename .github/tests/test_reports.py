
import pytest
import json

from django.urls import resolve
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import JsonResponse
from pytest_django.asserts import assertFormError, assertContains, assertTemplateUsed

from ptpud04 import views
from ptpud04.models import MotoElectrica

@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'dump_profesor.json')

# REPORT_TOP_CLIENTS_PATH = "/informes/top3_clientes/"

# '''Comprobamos que la URL de la vista del informe
#    de los 3 mejores clientes
#    es correcta y que devuelve un código 200'''
# def test_url_report_top_clientes(db, client):
#     resolver = resolve(REPORT_TOP_CLIENTS_PATH, urlconf='ptpud04.urls')
#     assert resolver.func == views.top3_cliente_report
#     response = client.get(REPORT_TOP_CLIENTS_PATH)
#     assert response.status_code == 200
#     assertTemplateUsed(response, 'ptpud04/informes/top3_clientes.html')
#     query_list = list(views.query_top3_clientes())
#     clientes_list = list(response.context['clientes'])
#     assert len(clientes_list) == len(query_list) == 3 \
#       and clientes_list == query_list

# def test_query_top_cliente(db):
#     clientes = views.query_top3_clientes()
#     assert isinstance(clientes, QuerySet)
#     assert len(clientes) == 3
#     clientes_list = list(clientes.values('id', 'user__username', 'saldo', 'sum_alquileres', 'alquileres'))
#     json_result = JsonResponse(clientes_list, safe=False).content
#     json_expected = b'[{"id": 3, "user__username": "daniela", "saldo": "5000.00", "sum_alquileres": "732.270000000000", "alquileres": 5}, {"id": 2, "user__username": "juan", "saldo": "100.99", "sum_alquileres": "51.8400000000000", "alquileres": 2}, {"id": 4, "user__username": "perica", "saldo": "10.01", "sum_alquileres": "18.0100000000000", "alquileres": 2}]'
#     assert json_result == json_expected



REPORT_TOP_BIKES_PATH = "/informes/top5_motos/"

'''Comprobamos que la URL de la vista del informe
   de las 5 mejores motos
   es correcta y que devuelve un código 200'''
def test_url_report_top_bikes(db, client):
    resolver = resolve(REPORT_TOP_BIKES_PATH, urlconf='ptpud04.urls')
    assert resolver.func == views.top5_moto_report
    response = client.get(REPORT_TOP_BIKES_PATH)
    assert response.status_code == 200
    assertTemplateUsed(response, 'ptpud04/informes/top5_motos.html')
    query_list = list(views.query_top5_motos())
    motos_list = list(response.context['motos'])
    assert len(motos_list) == len(query_list) == 5 \
      and motos_list == query_list

def test_query_top_bikes(db):
    motos = views.query_top5_motos()
    assert isinstance(motos, QuerySet)
    assert len(motos) == 5
    motos_list = list(motos.values('marca', 'modelo', 'tarifa_segundo', 'alquileres'))
    json_result = JsonResponse(motos_list, safe=False).content
    print(json_result)
    json_expected = b'[{"marca": "Aprilia", "modelo": "milia", "tarifa_segundo": "0.0016", "alquileres": 3}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002", "alquileres": 3}, {"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025", "alquileres": 2}, {"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001", "alquileres": 2}, {"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005", "alquileres": 2}]'
    assert json_result == json_expected

"""
Tests para el informe de maestro de detalle
"""

REPORT_MD_PATH = "/informes/maestro_detalle/"

def test_query_maestro_detalle_no_params(db):
    motos_expected = MotoElectrica.objects.all()
    motos_result = views.query_maestro_detalle(None, None)
    assert isinstance(motos_result, QuerySet)
    assert len(motos_expected) == len(motos_result)
    assert set(motos_expected) == set(motos_result)

"""
Test de assertions genéricas para el informe de maestro de detalle
"""
def assert_query_maestro_detalle(mm_filter, la_filter, expected_len, expected_data):
    motos_expected = MotoElectrica.objects.all()
    motos_result = views.query_maestro_detalle(mm_filter, la_filter)
    assert isinstance(motos_result, QuerySet)
    assert expected_len == len(motos_result)
    motos_list = list(motos_result.values('marca', 'modelo', 'tarifa_segundo'))
    result_data = JsonResponse(motos_list, safe=False).content
    assert expected_data == result_data

marca_modelo_samples = [
    ('Derbi', 1, b'[{"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025"}]'),
    ('v', 3, b'[{"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025"}, {"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]'),
    ('h', 5, b'[{"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001"}, {"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]'),
    ('FIGHTER', 1, b'[{"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}]'),
    ('ma', 2, b'[{"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001"}, {"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005"}]')
]
@pytest.mark.parametrize("mm_filter,expected_len, expected_data", marca_modelo_samples)
def test_query_maestro_detalle_marca_modelo_filter(db, mm_filter, expected_len, expected_data):
    assert_query_maestro_detalle(mm_filter, None, expected_len, expected_data)

# Probar el filtro de libre/alquilada
libre_alquilada_samples = [
    ('2', 2, b'[{"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025"}, {"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005"}]'),
    ('1', 6, b'[{"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001"}, {"marca": "Aprilia", "modelo": "milia", "tarifa_segundo": "0.0016"}, {"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]'),
    ('0', 8, b'[{"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025"}, {"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001"}, {"marca": "Aprilia", "modelo": "milia", "tarifa_segundo": "0.0016"}, {"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005"}, {"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]')
]
@pytest.mark.parametrize("la_filter, expected_len, expected_data", libre_alquilada_samples)
def test_query_maestro_detalle_libre_alquilada_filter(db, la_filter, expected_len, expected_data):
    assert_query_maestro_detalle(None, la_filter, expected_len, expected_data)


# Probar el filtro de libre/alquilada y marca/modelo
completo_samples = [
    ('','0', 8, b'[{"marca": "Derbi", "modelo": "Variant", "tarifa_segundo": "0.0025"}, {"marca": "Yamaha", "modelo": "lenta", "tarifa_segundo": "0.0001"}, {"marca": "Aprilia", "modelo": "milia", "tarifa_segundo": "0.0016"}, {"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005"}, {"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]'),
    ('d', '1', 3, b'[{"marca": "BMV", "modelo": "Thunder", "tarifa_segundo": "0.0100"}, {"marca": "Honda", "modelo": "fighter", "tarifa_segundo": "0.0068"}, {"marca": "Honda", "modelo": "VIP 2000", "tarifa_segundo": "5.5000"}]'),
    ('u', '2', 1, b'[{"marca": "Ducati", "modelo": "fumato", "tarifa_segundo": "0.0005"}]'),
    ('home', '2', 0, b'[]'),
    ('rico', '1', 0, b'[]'),
    ('ri', '1', 2, b'[{"marca": "Aprilia", "modelo": "milia", "tarifa_segundo": "0.0016"}, {"marca": "Kawasaki", "modelo": "aquachirri", "tarifa_segundo": "0.0002"}]')
]
@pytest.mark.parametrize("mm_filter, la_filter, expected_len, expected_data", completo_samples)
def test_query_maestro_detalle_completo_filter(db, mm_filter, la_filter, expected_len, expected_data):
    assert_query_maestro_detalle(mm_filter, la_filter, expected_len, expected_data)

'''Comprobamos que la URL de la vista de informes de maestro de detalle
   es correcta y que devuelve un código 200'''
def test_url_report_maestro_detalle(db, client):
    resolver = resolve(REPORT_MD_PATH, urlconf='ptpud04.urls')
    assert resolver.func == views.maestro_detalle_report
    response = client.get(REPORT_MD_PATH)
    assert response.status_code == 200
    assertTemplateUsed(response, 'ptpud04/informes/maestro_detalle.html')
    query_list = list(MotoElectrica.objects.all())
    motos_list = list(response.context['motos'])
    assert len(motos_list) == len(query_list) == 8 \
      and motos_list == query_list

completo_samples_reduced = [(a, b, c) for a, b, c, _ in completo_samples]
@pytest.mark.parametrize("mm_filter, la_filter, expected_len", completo_samples_reduced)
def test_view_maestro_detalle_completo(db, client, mm_filter, la_filter, expected_len):
    response = client.get(REPORT_MD_PATH, {'marca_modelo': mm_filter, 'libre_alquilada': la_filter})
    assert response.status_code == 200
    assertTemplateUsed(response, 'ptpud04/informes/maestro_detalle.html')
    motos_list = list(response.context['motos'])
    motos_query_list = list(views.query_maestro_detalle(mm_filter, la_filter))
    assert len(motos_list) == len(motos_query_list) == expected_len \
        and motos_list == motos_query_list
