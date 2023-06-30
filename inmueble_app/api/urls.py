"""
URL configuration for inmuebles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
# from inmueble_app.api.views import inmueble_list, inmueble_show
from inmueble_app.api.views import InmuebleList, InmuebleDetails, UserComment, InmuebleListFilter
from inmueble_app.api.views import CommentList, CommentDetails, CommentCreate
from inmueble_app.api.views import CompanyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('company', CompanyView, basename='company')

urlpatterns = [

    path('inmueble/', InmuebleList.as_view(), name='inmueble-list'),
    path('inmueble/list/', InmuebleListFilter.as_view(), name='inmueble'),
    path('inmueble/<int:pk>/', InmuebleDetails.as_view(), name='inmueble-detail'),

    path('', include(router.urls)),
    # path('company/', CompanyList.as_view(), name='company-list'),
    # path('company/<int:pk>/', CompanyDetails.as_view(), name='company-detail'),

    # path('comment/', CommentGAV.as_view(), name='comment-list'),
    path('inmueble/<int:pk>/comment-create/', CommentCreate.as_view(), name='comment-create'),
    path('inmueble/<int:pk>/comment/', CommentList.as_view(), name='comment-list'),
    path('inmueble/comment/<int:pk>/', CommentDetails.as_view(), name='comment-detail'),

    path('inmueble/comments/', UserComment.as_view(), name='user-comment-detail'),


]
