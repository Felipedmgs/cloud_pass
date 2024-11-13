from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView  
from app_sistema import views
from app_sistema.views import CustomLogoutView, login_view, home, register_password, list_credentials


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),  # Adicionando a URL para login
    path('index.html', views.index, name='index.html'),
    path('home/', views.home, name='home'),
    path('register-password/', views.register_password, name='register_password'),
    path('list-credentials/', views.list_credentials, name='list_credentials'),    
    path('', CustomLogoutView.as_view(), name='logout'),
]

