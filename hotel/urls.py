from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('cadastrar_hotel/', views.cadastrar_hotel, name="cadastrar_hotel"),
    path('hotel/<int:id>/', views.hotel, name="hotel"),
    path('seus_hoteis/', views.seus_hoteis, name="seus_hoteis"),
    path('visitas/', views.visitas, name="visitas"),
    path('hoteis_reservados/', views.hoteis_reservados, name="hoteis_reservados"),
    path('cancelar_visita/<int:id>/', views.cancelar_visita, name="cancelar_visita"),
    path('excluir_visita/<int:id>/', views.excluir_visita, name="excluir_visita"),
    path('hotel_favoritos/<int:id>/', views.hotel_favoritos, name="hotel_favoritos"),
    path('favoritos/', views.favoritos, name="favoritos"),
]

