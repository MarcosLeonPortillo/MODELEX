import datetime
import math
import pytz

from django.shortcuts import render



# Create your views here.
def welcome(request):
    return render(request, 'ptpud04/index.html')


# Espacio para la vista maestro_detalle
def maestro_detalle_report():
    pass


def query_maestro_detalle(marca_modelo, libre_alquilada):
    """ 
    El método debe devolver un objeto de tipo QuerySet a partir del parámetro
    motos.
    Se requiere que la consulta devuelva las motos que cumplan los siguientes criterios:
    - Si se ha introducido un valor en el campo marca_modelo, se debe filtrar por marca o modelo
    - Si se ha seleccionado la opción 'Libre', se deben devolver las motos que no estén alquiladas
    - Si se ha seleccionado la opción 'Alquilada', se deben devolver las motos que estén alquiladas
    - Si no se ha seleccionado ninguna opción, se deben devolver todas las motos
    - Ayudas: Se puede usar la función Q para construir la consulta. 
      Puede resultar de ayuda el método distinct() si se producen resultados duplicados
      Puede resultar de ayuda el método exclude() para sacar de la consulta
      resultados que cumplan una condición.
      Manual: DB - Consultas - Búsqueda compleja con consultas Q
      Si quiero los usuarios cuyo nombre empieza por A o por B:
        filtro = Q(nombre__startswith='A') | Q(nombre__startswith='B'
        Usuario.objects.filter(filtro)
    """
    return None


# Espacio para la vista top3_cliente
def top3_cliente_report():
    pass


def query_top3_clientes():
    """ 
    El método debe devolver un objeto de tipo QuerySet a partir del Model Usuario.
    Se requiere que la consulta devuelva la suma del coste de los alquileres 
    de cada cliente en un campo llamado 'sum_alquileres'
    y el número de alquileres en un campo llamado 'alquileres'
    Se espera el uso de la función annotate
    """
    return None


# Espacio para la vista top5_moto
def top5_moto_report():
    pass


def query_top5_motos():
    """ 
    El método debe devolver un objeto de tipo QuerySet a partir del Model MotoElectrica.
    Se requiere que la consulta devuelva la cantidad de veces que ha sido
    alquilada cada moto en un campo llamado 'alquileres'
    Se espera el uso de la función annotate
    """
    return None


#Espacio para la vista alquilar
def alquilar():
    pass
 
 
# Espacio para la vista liberar
def liberar():
    """
    Pistas:
    - Los errores se devuelven a través del objeto Http404
    - El método deve devolver al template los objetos moto y alquiler
    - Se debe usar una función de redondeo ya proporcionada en el código
    - Las fechas deben de tener timezones y no ser "naive" para ello
      se puede usar la función pytz.utc.localize({datetime_object})
    
    """
    pass

def round_up(value, decimals=2):
    """
    Rounds up a given value to the specified number of decimal places.

    Args:
        value (float): The value to be rounded up.
        decimals (int, optional): The number of decimal places to round up to. Defaults to 2.

    Returns:
        float: The rounded up value.
    """
    multiplier = 10 ** decimals
    return math.ceil(value * multiplier) / multiplier