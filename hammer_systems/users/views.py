from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from users.serializers import (
    UserProfileSerializer,
    UserInviteCodeSerializer,
    CreateUserSerializer
)
from users.models import UsersProfile


class UsersViewSet(viewsets.ModelViewSet):
    """ViewSet для профиля полязователя"""

    queryset = UsersProfile.objects.all()
    serializer_class = UserProfileSerializer()
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.action == 'registrate_user':
            return UserProfileSerializer
        if self.action == 'activate_invite_code':
            return UserInviteCodeSerializer
        return UserProfileSerializer

    @action(
        detail=True,
        methods=('post',),
        url_path=r'registrate_user'
    )
    def registrate_user(self, request):
        """
        Запрос к эндпоинту /registrate_user/.
        Метод для регистрации нового пользователя.
        """

        phone_number = request.data.get('phone_number')
        if UsersProfile.objects.filter(phone_number=phone_number).exists():
            return Response(
                {'message': 'Пользователь уже зарегистрирован'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Пользователь успешно зарегистрирован',
                 'invited_code': user.invite_code},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('get'),
        url_path=r'profile_user'
    )
    def profile_user(self, request):
        """
        Запрос к эндпоинту /profile_user/.
        Получения профиля пользователя.
        """
        user = request.user
        serializer = UserProfileSerializer(user, contex={'request': request})
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('post'),
        url_path=r'activate_invite_code'
    )
    def activate_invite_code(self, request):
        """
        Запрос к эндпоинту /activate_invite_code/.
        Метод для активации кода в личном кабинете пользователя.
        """
        user = request.user
        invite_code_serializer = UserInviteCodeSerializer(
            data=request.data, context={'request': request}
        )
        if invite_code_serializer.is_valid():
            code = request.data.get('auth_code')
            try:
                invite_code_serializer.check_activate_referal_code(code)
            except serializers.ValidationError as e:
                return Response(
                    {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

            user = request.user
            user.auth_code = code
            user.save()

            serializer = UserProfileSerializer(
                user, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
