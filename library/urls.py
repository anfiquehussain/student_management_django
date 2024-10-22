from django.urls import path
from . import views

urlpatterns = [
    path('',views.LibraryView.as_view(),name='library'),
    path('manage_library',views.LibraryManageView.as_view(),name='library_manage'),

    path('library/create',views.CreateLibraryView.as_view(),name='create_library'),
    path('library/<int:pk>/edit',views.EditLibraryView.as_view(),name='edit_library'),
    path('library/<int:pk>/delete',views.DeleteLibraryView.as_view(),name='delete_library'),
    path('search_library',views.LibrarySearchView.as_view(),name='search_library'),


    path('manage_book',views.BookManageView.as_view(),name='book_manage'),
    path('book/create',views.CreateBookView.as_view(),name='create_book'),
    path('book/<int:pk>/edit',views.EditBookView.as_view(),name='edit_book'),
    path('book/<int:pk>/delete',views.DeleteBookView.as_view(),name='delete_book'),
    path('search_book',views.BookSearchView.as_view(),name='search_book'),


]