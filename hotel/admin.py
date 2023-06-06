from django.contrib import admin
from .models import DiaSemana, Horario, Visitas, Hotel, HotelFavorito, Estrelas, Cidades, QuartosHotel


admin.site.register(Hotel)
admin.site.register(HotelFavorito)
admin.site.register(DiaSemana)
admin.site.register(Estrelas)
admin.site.register(Visitas)
admin.site.register(Cidades)
admin.site.register(Horario)
admin.site.register(QuartosHotel)