from .models import Users
from django.contrib import admin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import admin as django_user_admin


@admin.register(Users)
class UsersAdmin(django_user_admin.UserAdmin):
    # Sobrescrever forms
    form = UserChangeForm
    add_form = UserCreationForm
    # Sobrescrever model
    model = Users

    # Alterar/Adicionar campos

    fieldsets = django_user_admin.UserAdmin.fieldsets + (
        ('Personal data', {'fields': ("zip_code", "address", "state", "city", "neighborhood", "cell_phone", "telephone", "recovery_email")}),
    )
