from django.shortcuts import render, redirect
from .utils import validate_password, validate_fields
from django.contrib.auth import login as logar, logout
from django.contrib.auth.decorators import login_required
from .models import Users
from .backends import CustomBackend
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse

def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/hotel/home/')

        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        zip_code = request.POST.get('zip_code')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        neighborhood = request.POST.get('neighborhood')
        cell_phone = request.POST.get('cell_phone')
        telephone = request.POST.get('telephone')
        recovery_email = request.POST.get('recovery_email')

        if not validate_fields(username, surname, email, password, confirm_password, zip_code, address, state, city, neighborhood, cell_phone, recovery_email):
            messages.add_message(request, constants.ERROR, 'Campos inválidos!')
            return redirect('/auth/register/')

        if not validate_password(request, password, confirm_password):
            return redirect('/auth/register/')

        if Users.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'Email  já existe!')
            return redirect('/auth/register/')

        try:
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                zip_code=zip_code,
                address=address,
                state=state,
                city=city,
                neighborhood=neighborhood,
                cell_phone=cell_phone,
                telephone=telephone,
                recovery_email=recovery_email,
            )
            user.first_name = surname
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastrado(a) com sucesso!')
            return redirect('/auth/login/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return redirect('/auth/register/')

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/hotel/home/')

        status = request.GET.get('status')
        context = {
            'status': status
        }
        return render(request, 'login.html', context=context)
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not validate_fields(email, password):
            messages.add_message(request, constants.ERROR, 'Campos inválidos')
            return redirect('/auth/login/')
        
        usuario = CustomBackend.authenticate(request, request, username=email, password=password)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'E-mail ou senha inválidos')
            return redirect('/auth/login/')
        else:
            logar(request, usuario)
            return redirect('/hotel/home/')

@login_required(login_url='/auth/login/?status=1')
def exit(request):
    logout(request)
    messages.add_message(request, constants.INFO, 'Volte sempre')
    return redirect('/auth/login/')