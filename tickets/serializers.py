from rest_framework import serializers
from .models import Ticket
from users.models import User


class TicketSerializer(serializers.ModelSerializer):
    """Сериализатор для получения заявок"""

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


class TicketCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки пользователем"""

    class Meta:
        model = Ticket

        fields = (
            'title',
            'description',
        )


class TicketUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения заявки сотрудниками поддержки"""

    class Meta:
        model = Ticket

        fields = (
            'status',
            'assigned_to',
        )

    def validate_assigned_to(self, value):
        if value is None:
            return value

        # Запрет на назначение исполнителем заявки обычного пользователя
        if value.role != User.Role.SUPPORT:
            raise serializers.ValidationError(
                'Исполнителем может быть только сотрудник поддержки.'
            )

        return value

    def validate(self, attrs):
        current_status = self.instance.status
        new_status = attrs.get('status', current_status)
        assigned_to = attrs.get('assigned_to', self.instance.assigned_to)

        # Проверка на переходы заявки из одного состояния в другое
        if new_status != current_status:
            allowed = Ticket.ALLOWED_TRANSITIONS[current_status]

            if new_status not in allowed:
                raise serializers.ValidationError(
                    f'Нельзя перевести заявку из '
                    f'{current_status} в {new_status}'
                )

        # Запрет на изменение закрытой заявки
        if self.instance.status == Ticket.Status.DONE:
            raise serializers.ValidationError(
                'Закрытая заявка не может быть изменена.'
            )

        # бизнес-правило: нельзя закрыть без исполнителя
        if (
            new_status == Ticket.Status.DONE
            and assigned_to is None
        ):
            raise serializers.ValidationError(
                'Нельзя закрыть заявку без исполнителя.'
            )

        # бизнес-правило: нельзя в IN_PROGRESS без исполнителя
        if (
                new_status == Ticket.Status.IN_PROGRESS
                and assigned_to is None
        ):
            raise serializers.ValidationError(
                "Для начала работы нужно назначить исполнителя."
            )

        return attrs