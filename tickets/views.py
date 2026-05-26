from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from users.models import User
from .models import Ticket
from .permissions import TicketPermission
from .serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
)


class TicketViewSet(ModelViewSet):
    """Представление для обработки GET, POST, PUT и PATCH запросов"""

    permission_classes = [TicketPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer

        if self.action in (
            'update',
            'partial_update',
        ):
            return TicketUpdateSerializer

        return TicketSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role in (
            User.Role.ADMIN,
            User.Role.SUPPORT,
        ):
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
