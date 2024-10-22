from django import forms
from .models import Book,LibraryRecord

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title Name',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Author Name',
            }),
        }

class LibraryRecordForm(forms.ModelForm):
    class Meta:
        model = LibraryRecord
        fields = ['student', 'book', 'borrowed_on', 'returned_on', 'return_status']
        
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select Student',
            }),
            'book': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select Book',
            }),
            'borrowed_on': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Borrowed Date',
            }),
            'returned_on': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Returned Date (if returned)',
            }),
            'return_status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
