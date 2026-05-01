from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('internships/', views.internships , name='internships'),
    path('profile/', views.profile, name='profile'),
    path('apply/<int:id>/', views.apply_internship, name='apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
]