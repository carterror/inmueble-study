from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
<<<<<<< HEAD
from user_app.api.views import logoutView, registerView, loginView, sessionView
=======
from user_app.api.views import logoutView, registerView
>>>>>>> parent of 25b4be5 (primer deploy dajngo)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

urlpatterns = [

    path('login/', obtain_auth_token, name='login'),
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),
    path('session/', sessionView, name='session'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
