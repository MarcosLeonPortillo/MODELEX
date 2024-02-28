from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # Los siguientes paths estan pensados para ir
    # descomentandolos y completandolos a medida que se vayan implementando
    path('informes/maestro_detalle/', views.query_maestro_detalle, name='maestro_detalle'),
    # path('', , name='top3_cliente'),
    path('informes/top5_motos/', views.query_top5_motos, name='top5_moto'),
    path('alquila/<int:pk>/', views.alquilar, name='alquila'),
    path('libera/<int:pk>/', views.liberar, name='libera'),
]
