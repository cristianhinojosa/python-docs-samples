from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("", include("api.urls")),
    path("documentation/", schema_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    #path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
