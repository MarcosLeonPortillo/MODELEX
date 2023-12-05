from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # Los siguientes paths estan pensados para ir
    # descomentandolos y completandolos a medida que se vayan implementando
    path('localhost:8000/informes/maestro_detalle/', views.query_maestro_detalle, name='maestro_detalle'),
    # path('', , name='top3_cliente'),
    path('localhost:8000/informes/top5_motos/', views.query_top5_motos, name='top5_moto'),
    # path('', , name='alquila'),
    # path('', , name='libera'),
]
