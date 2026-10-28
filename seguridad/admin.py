from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Rol, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # agrega el campo "rol" al formulario del admin
    fieldsets = UserAdmin.fieldsets + (
        ('Rol del sistema', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol del sistema', {'fields': ('rol',)}),
    )
    list_display = ('username', 'email', 'rol', 'is_active')


admin.site.register(Rol)
