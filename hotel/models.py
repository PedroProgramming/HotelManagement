from django.db import models
from authentication.models import Users
from django.utils import timezone
    
class Cidades(models.Model):
    cidades = models.CharField(max_length=150)

    def __str__(self):
        return self.cidades
    
    class Meta:
        verbose_name_plural = "Cidades"

class Estrelas(models.Model):
    estrelas = models.CharField(max_length=5)

    def __str__(self):
        return self.estrelas
    
    class Meta:
        verbose_name_plural = "Estrelas"
    
class DiaSemana(models.Model):
    dias = models.CharField(max_length=50)

    def __str__(self):
        return self.dias

class Horario(models.Model):
    horario = models.CharField(max_length=100)

    def __str__(self):
        return self.horario
    
class QuartosHotel(models.Model):
    quartos = models.CharField(max_length=50)

    def __str__(self):
        return self.quartos

class Hotel(models.Model):

    usuario = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    imagem = models.ImageField(upload_to='img_hoteis')
    nome = models.CharField(max_length=150)
    preco = models.FloatField()
    endereco = models.CharField(max_length=150)
    estrelas = models.ForeignKey(Estrelas, on_delete=models.DO_NOTHING)
    cidade = models.ForeignKey(Cidades, on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=11)
    tipo_quarto_hotel = models.ForeignKey(QuartosHotel, on_delete=models.DO_NOTHING)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Visitas(models.Model):
    agendar = (
        ('A', 'Agendado'),
        ('Ca', 'Cancelando'),
        ('C', 'Cancelado'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    dias = models.ForeignKey(DiaSemana, on_delete=models.DO_NOTHING)
    horarios = models.ForeignKey(Horario, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=2,
        choices=agendar,
        default='A',
        )
    
    def __str__(self):
        return self.hotel.nome
    
    class Meta:
        verbose_name_plural = "Visitas"


class HotelFavorito(models.Model):
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    hotel_favorito = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.hotel_favorito.nome