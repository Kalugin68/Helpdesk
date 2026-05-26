from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket

        fields = (
            'id',
            'title',
            'description',
            'status',
            'author',
            'assigned_to',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'author',
            'created_at',
            'updated_at',
        )