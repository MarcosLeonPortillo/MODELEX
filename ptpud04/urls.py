from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # Los siguientes paths estan pensados para ir
    # descomentandolos y completandolos a medida que se vayan implementando
    # path('', , name='maestro_detalle'),
    # path('', , name='top3_cliente'),
    # path('',, name='top5_moto'),
    # path('', , name='alquila'),
    # path('', , name='libera'),
]
