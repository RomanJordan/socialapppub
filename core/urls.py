from django.urls import path, include
from . import views
from .views import index, RegisterView, ProfileView, ProfileEdit, UpdateProfile, get_user_profile, UserViewSet, ProfileViewSet
from django.contrib.auth import views as auth_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('u/<str:username>/', ProfileView.as_view(), name='profile'),
    # path('u/<str:username>/', views.profile, name='profile'),
    path('edit/', views.ProfileEdit, name='edit_profile'),
    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]