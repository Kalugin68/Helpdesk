from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_dispay = (
        'id',
        'title',
        'description',
        'status',
        'author',
        'assigned_to',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
    )

    ordering = (
        'status',
        '-created_at',
    )