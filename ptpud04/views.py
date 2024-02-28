import datetime
import math
import pytz
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from .models import Usuario, MotoElectrica, Alquiler
from django.db.models import Count, Sum, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render



# Create your views here.
def welcome(request):
    return render(request, 'ptpud04/index.html')


# Espacio para la vista maestro_detalle
def maestro_detalle_report(request):
    marca_modelo = request.GET.get('marca_modelo', '')
    libre_alquilada = request.GET.get('libre_alquilada', '')
    motos = query_maestro_detalle(marca_modelo, libre_alquilada)
    return render(request, 'ptpud04/informes/maestro_detalle.html', {'motos': motos})


def query_maestro_detalle(marca_modelo, libre_alquilada):
    query = Q()

    if marca_modelo:
        query |= Q(marca__icontains=marca_modelo) | Q(modelo__icontains=marca_modelo)

    if libre_alquilada == 'libre':
        query &= Q(alquiler__isnull=True)
    elif libre_alquilada == 'alquilada':
        query &= Q(alquiler__isnull=False)

    motos = MotoElectrica.objects.filter(query).distinct()
    return motos


# Espacio para la vista top3_cliente
def top3_cliente_report(request):
    clientes = query_top3_clientes()
    return render(request, 'ptpud04/informes/top3_clientes.html', {'clientes': clientes})


def query_top3_clientes():
    return Usuario.objects.annotate(
        sum_alquileres=Sum('alquiler__coste'),
        alquileres=Count('alquiler')
    ).order_by('-sum_alquileres')[:3]


# Espacio para la vista top5_moto
def top5_moto_report(request):
    motos = query_top5_motos()
    return render(request, 'ptpud04/informes/top5_motos.html', {'motos': motos})


def query_top5_motos():
    return MotoElectrica.objects.annotate(alquileres=Count('alquiler')).order_by('-alquileres')[:5]


# Espacio para la vista alquilar
def alquilar():
    pass


# Espacio para la vista liberar
def liberar(request):
    moto_id = request.GET.get('moto_id')
    alquiler_id = request.GET.get('alquiler_id')

    try:
        moto = MotoElectrica.objects.get(pk=moto_id)
        alquiler = Alquiler.objects.get(pk=alquiler_id)

        if alquiler.moto != moto or alquiler.devuelta:
            raise Http404("La moto o el alquiler no son válidos.")

        # Realizar las operaciones necesarias para liberar la moto
        alquiler.devuelta = True
        alquiler.fecha_devolucion = timezone.now()
        alquiler.coste = round_up(
            (alquiler.fecha_devolucion - alquiler.fecha_alquiler).total_seconds() * moto.tarifa_segundo
        )
        alquiler.save()

        messages.success(request, f"Se ha liberado la moto {moto.marca} {moto.modelo}. Coste: {alquiler.coste}€.")
    except MotoElectrica.DoesNotExist:
        raise Http404("La moto no existe.")
    except Alquiler.DoesNotExist:
        raise Http404("El alquiler no existe.")

    return redirect('ptpud04:index')


def round_up(value, decimals=2):
    multiplier = 10 ** decimals
    return math.ceil(value * multiplier) / multiplier