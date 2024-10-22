from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from accounts.mixins import RoleRequiredMixin
from .models import *
from .forms import BookForm,LibraryRecordForm
from django.urls import reverse_lazy
from students.models import Class

# Create your views here.
class LibraryView(RoleRequiredMixin,TemplateView):
    allowed_roles = ['Librarian','Admin']
    template_name='library/library.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.all().count()
        context['total_books'] = Book.objects.all().count()
        context['total_records'] = LibraryRecord.objects.all().count()
        return context


"""
Library Records
"""

class LibraryManageView(RoleRequiredMixin,ListView):
    allowed_roles = ['Librarian','Admin']
    template_name='library/library/library_manage.html'
    model = LibraryRecord
    context_object_name = 'libraries'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classlist'] = Class.objects.all()
        return context

class CreateLibraryView(RoleRequiredMixin,CreateView):
    allowed_roles = ['Librarian','Admin']
    model = LibraryRecord
    form_class = LibraryRecordForm 
    template_name = 'library/library/create_library.html'
    success_url = reverse_lazy('library_manage')


class EditLibraryView(RoleRequiredMixin,UpdateView):
    allowed_roles = ['Librarian','Admin']
    model = LibraryRecord
    form_class = LibraryRecordForm 
    template_name = 'library/library/edit_library.html'
    success_url = reverse_lazy('library_manage')


class DeleteLibraryView(RoleRequiredMixin,DeleteView):
    allowed_roles = ['Librarian', 'Admin']
    model = LibraryRecord
    def post(self, request, pk):
        lb = get_object_or_404(LibraryRecord, pk=pk)
        lb.delete()
        return redirect('library_manage')
    

from django.views.generic import ListView
from django.http import JsonResponse
from .models import LibraryRecord

class LibrarySearchView(ListView):
    def get(self, request, *args, **kwargs):
        # Retrieve query parameters
        query = request.GET.get('q', '')
        class_name = request.GET.get('class', '')
        gender = request.GET.get('gender', '')
        age = request.GET.get('age', '')
        address = request.GET.get('address', '')
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        borrowed_on = request.GET.get('borrowed_on', '')
        return_status = request.GET.get('return_status', '')
        returned_on = request.GET.get('returned_on', '')

        # Start with all library records
        library = LibraryRecord.objects.all()

        # Filter library records based on the query parameters
        if query:
            library = library.filter(student__full_name__icontains=query)
        if class_name:
            library = library.filter(student__class_name__class_name=class_name.upper())
        if address:
            library = library.filter(student__address__icontains=address)
        if gender:
            library = library.filter(student__gender=gender)
        if age.isdigit():
            library = library.filter(student__age=int(age))
        if title:
            library = library.filter(book__title__icontains=title)
        if author:
            library = library.filter(book__author__icontains=author)
        if borrowed_on:
            library = library.filter(borrowed_on=borrowed_on)
        if return_status:
            library = library.filter(return_status=bool(int(return_status)))
        if returned_on:
            library = library.filter(returned_on=returned_on)

        # Prepare the response data
        library_data = list(library.values(
            'id',
            'student__full_name',
            'student__class_name__class_name',
            'student__age',
            'student__gender',
            'student__address',
            'student__contact_number',
            'book__title',
            'borrowed_on',
            'returned_on',
            'return_status'
        ))

        return JsonResponse({'libraries': library_data})


"""
Books
"""

class BookManageView(RoleRequiredMixin,ListView):
    allowed_roles = ['Librarian','Admin']
    model = Book
    template_name = 'library/book/book_manage.html'
    context_object_name = 'books'

class CreateBookView(RoleRequiredMixin,CreateView):
    allowed_roles = ['Librarian','Admin']
    model = Book
    form_class = BookForm
    template_name = 'library/book/create_book.html'
    success_url = reverse_lazy('book_manage')

class EditBookView(RoleRequiredMixin,UpdateView):
    allowed_roles = ['Librarian','Admin']
    model = Book
    form_class = BookForm
    template_name = 'library/book/edit_book.html'
    success_url = reverse_lazy('book_manage')


class DeleteBookView(RoleRequiredMixin,DeleteView):
    allowed_roles = ['Librarian', 'Admin']
    model = Book
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_manage')


from django.http import JsonResponse

class BookSearchView(ListView):
    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')

        # Filter books by title and author (case-insensitive match)
        books = Book.objects.all()
        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__icontains=author)

        # Prepare the data for JSON response
        books_data = list(books.values('id', 'title', 'author'))  # Convert queryset to list of dictionaries

        return JsonResponse({'books': books_data})
