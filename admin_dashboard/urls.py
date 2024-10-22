from django.urls import path
from . import views

urlpatterns = [
    path('',views.AdminDashBoardView.as_view(),name='admin_dashboard'),
    path('manage_staff',views.ManageStaffView.as_view(),name='manage_staff'),
    path('manage_librarian',views.ManageLibrarianView.as_view(),name='manage_librarian'),
    path('search_users', views.UserSearchView.as_view(), name='search_users'),
]