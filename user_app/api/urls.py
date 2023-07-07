from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import logoutView, registerView, loginView


urlpatterns = [

    # path('login/', obtain_auth_token, name='login'),
    path('login-app/', loginView, name='login-app'),
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),


]
