from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()

    serializer_class = TicketSerializer
