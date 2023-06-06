import re
from django.contrib import messages
from django.contrib.messages import constants

def validate_password(request, password, confirm_password):

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'Senhas diferentes')
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Senha não contem letra maiuscula')
        return False
    
    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Senha não contem letra minuscula')
        return False

    if not re.search('[1-5]', password):
        messages.add_message(request, constants.ERROR, 'Senha não contem números de 1 até 5')
        return False

    return True

def validate_fields(*args):
    return all(arg.strip() != '' for arg in args)