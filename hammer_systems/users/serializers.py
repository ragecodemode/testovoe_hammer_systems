import re

from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.genrate_invite_code import create_invite_code


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Регистрацитя пользователя."""

    class Meta:
        model = User
        fields = ('phone_number', 'ivite_code', 'auth_code',)

    def create(self,  validated_data):
        phone_number = validated_data.pop('phone_number')

        if not re.match(r'^\+?\d{8,15}$', phone_number) and len(
            phone_number
        ) > 14:
            raise serializers.ValidationError(
                {'message': 'Введиете правильный номер телефона'}
            )

        invite_code = create_invite_code(6)
        validated_data['invite_code'] = invite_code

        return User.objects.create(** validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для прфиля пользователя"""
    all_invited_codes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'all_invited_codes',)

    def get_all_invited_codes(self, codes):
        """
        Метод для получения списка инвайт кодов
        для текущего пользователя
        """
        code = User.objects.filter(
            codes=codes.ivite_code
            ).values_list(
                'phone_number', flat=True
            )
        return code


class UserInviteCodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проверки:
    корректности, активации и существования инвайт кода
    """

    class Meta:
        model = User
        fields = ('auth_code',)

    def check_activate_referal_code(self, code):
        """
        Метод для проверки на активацию инвайт кода
        у текущего пользователя
        """
        user = self.context["request"].user

        if not User.objects.filter(invite_code=code).exists():
            raise serializers.ValidationError(
                {'message': 'Такого инвайт кода не существует!'}
            )

        if user.auth_code:
            raise serializers.ValidationError(
                {'message':
                    f'Вы вводите этот {user.auth_code} реферальный код!'}
            )

        if code != user.auth_code:
            raise serializers.ValidationError(
                {'message': 'Инвайт коды не совпададаюи с вашим инвайт кодом'}
            )
        return code
