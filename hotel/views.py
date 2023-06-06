from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hotel, Cidades, HotelFavorito, Estrelas, QuartosHotel, Visitas, DiaSemana, Horario
from .utils import validate_fields
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import clear_url_caches


@login_required(login_url='/auth/login/')
def home(request):

    if request.method == 'GET':
        hotel_nome = request.GET.get('search')
        
        cidades = Cidades.objects.all()
        estrelas = Estrelas.objects.all()
        quartos = QuartosHotel.objects.all()

        preco_minimo = request.GET.get('preco_minimo')
        preco_maximo = request.GET.get('preco_maximo')
        quarto = request.GET.get('quarto')
        estrela = request.GET.get('estrela')
        cidade = request.GET.get('cidade')

        if preco_minimo or preco_maximo or quarto or estrela or cidade:
            if not preco_minimo:
                preco_minimo = 0
            
            if not preco_maximo:
                preco_maximo = 999999999

            hotel = Hotel.objects.filter(preco__gte=preco_minimo).filter(preco__lte=preco_maximo).filter(tipo_quarto_hotel=quarto).filter(estrelas=estrela).filter(cidade=cidade)
        else:
            hotel = Hotel.objects.all()    

        if hotel_nome:
            hotel = Hotel.objects.filter(nome__icontains=hotel_nome)

        context = {
            'hotel': hotel,  
            'estrelas': estrelas,
            'cidades': cidades,
            'quartos': quartos,
        }

        return render(request, 'home.html', context=context) 

@login_required(login_url='/auth/login/')
def cadastrar_hotel(request):
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        imagem = request.FILES.get('imagem')
        preco = request.POST.get('preco')
        endereco = request.POST.get('endereco')
        estrela = request.POST.get('estrela')
        cidade = request.POST.get('cidade')
        celular = request.POST.get('celular')
        tipo = request.POST.getlist('tipo')
        print(celular)

        if not validate_fields(nome, preco, endereco):
            messages.add_message(request, constants.ERROR, 'Campos inválidos')
            return redirect('/hotel/home/')

        if not imagem != None:
            messages.add_message(request, constants.ERROR, 'Nenhuma imagem selecionada')
            return redirect('/home/hotel/')

        if not len(celular) == 11:
            messages.add_message(request, constants.ERROR, 'Celular menos ou mais que 11 digitos')
            return redirect('/hotel/home/')
        
        try:
            hotel = Hotel(
                usuario=request.user,
                imagem=imagem,
                nome=nome,
                preco=preco,
                endereco=endereco,
                estrelas_id=estrela,
                cidade_id=cidade,
                numero=celular,
                tipo_quarto_hotel_id=tipo[0],
            )
            hotel.save()

            messages.add_message(request, constants.SUCCESS, 'Hotel cadastrado com sucesso')
            return redirect('/hotel/home/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/hotel/home/')

@login_required(login_url='/auth/login/')
def hotel(request, id):
    hotel_view = get_object_or_404(Hotel, id=id)
    horarios = Horario.objects.all()
    dias = DiaSemana.objects.all()
    hotel_favorito = HotelFavorito.objects.filter(user=request.user, hotel_favorito=hotel_view)
    
    segestao_hotel = Hotel.objects.filter(cidade=hotel_view.cidade).exclude(id=id)[:2]

    context = {
        'hotel_view': hotel_view,
        'horarios': horarios,
        'dias': dias,
        'hotel_favorito': hotel_favorito,
        'segestao_hotel': segestao_hotel,
    }
    return render(request, 'view_hotel.html', context=context)

@login_required(login_url='/auth/login/')
def seus_hoteis(request):
    hoteis_cadastrados = Hotel.objects.all().filter(usuario=request.user)

    context = {
        'hoteis_cadastrados': hoteis_cadastrados,
    }
    return render(request, 'seus_hoteis.html', context=context)

@login_required(login_url='/auth/login/')
def visitas(request):

    hotel = request.POST.get('hotel')
    dias = request.POST.get('dias')
    horarios = request.POST.get('horarios')

    try:
        visita = Visitas(
            hotel_id=hotel,
            user=request.user,
            dias_id=dias,
            horarios_id=horarios,
        )
        visita.save()

        messages.add_message(request, constants.SUCCESS, 'Visita marcada')
        return redirect(f'/hotel/hoteis_reservados/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect(f'/hotel/hotel/{hotel}/')

@login_required(login_url='/auth/login/')
def hoteis_reservados(request):
    reservas = Visitas.objects.all().filter(user=request.user)
    context = {
        'reservas': reservas,
    }
    return render(request, 'reservas.html', context=context)

@login_required(login_url='/auth/login/')
def cancelar_visita(request, id):
    visita = get_object_or_404(Visitas, id=id)
    visita.status = 'C'
    visita.save()
    return redirect('/hotel/hoteis_reservados/')

@login_required(login_url='/auth/login/')
def excluir_visita(request, id):
    del_visita = get_object_or_404(Visitas, id=id)
    del_visita.delete()
    messages.add_message(request, constants.INFO, 'Reserva excluida com sucesso!')
    return redirect('/hotel/hoteis_reservados/')

@login_required(login_url='/auth/login/')
def hotel_favoritos(request, id):
    user = request.user
    hotel = Hotel.objects.get(id=id)

    hotel_like = HotelFavorito.objects.filter(user=user, hotel_favorito=id)
    if not hotel_like:
        hotel_like = HotelFavorito.objects.create(user=user, hotel_favorito=hotel)
        hotel_like.save()
        messages.add_message(request, constants.SUCCESS, 'Adiconado aos favoritos')
        return redirect(f'/hotel/hotel/{hotel.id}/')
    else:
        hotel_like = HotelFavorito.objects.filter(user=user, hotel_favorito=hotel).delete()
        messages.add_message(request, constants.WARNING, 'Removido dos favoritos')
        return redirect(f'/hotel/hotel/{hotel.id}/')

@login_required(login_url='/auth/login/')
def favoritos(request):
    favotiros_hotel = HotelFavorito.objects.all().filter(user=request.user)

    context = {
        'favotiros_hotel': favotiros_hotel,
    }
    return render(request, 'favoritos.html', context=context)