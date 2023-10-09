from django.contrib import admin

from .models import *


class TicketsTableAdmin(admin.ModelAdmin):
    list_display = (
        'nick_name', 'currency', 'coin', 'trade_type', 'exchange_id', 'time_create',
        'link',)  # —> отображение столбиков
    list_display_links = ('nick_name',)  # —> ссылки для перехода к элементу
    search_fields = ('nick_name', 'exchange_id')  # —> поиск по этим элементам
    list_filter = ('time_create', 'exchange_id')  # —> сайдбар для сортировки по данным айтемам


admin.site.register(TicketsTable, TicketsTableAdmin)
