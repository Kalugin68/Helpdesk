from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from users.models import User
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import TicketPermission


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    permission_classes = [TicketPermission]

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
