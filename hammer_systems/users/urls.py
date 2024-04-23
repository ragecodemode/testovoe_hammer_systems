from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UsersViewSet


app_name = 'hammer_systems'
router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
