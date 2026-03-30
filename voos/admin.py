from django.contrib import admin
from .models import Voo, Passageiro, Reserva


@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ['numero', 'origem', 'destino', 'data_partida', 'status']
    list_filter = ['status', 'origem', 'destino']
    search_fields = ['numero', 'origem', 'destino']


@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email']
    search_fields = ['nome', 'cpf', 'email']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['voo', 'passageiro', 'assento', 'status', 'data_reserva']
    list_filter = ['status']
    search_fields = ['assento', 'passageiro__nome', 'voo__numero']
