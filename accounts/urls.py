from django.urls import path
from . import views

urlpatterns = [
    path('',views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/create', views.UserCreateView.as_view(), name='create_user'),
    path('user/<int:pk>/edit/', views.UserEditView.as_view(), name='user-edit'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]