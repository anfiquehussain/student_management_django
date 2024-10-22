from django import forms
from .models import *  # Import your Class model
import re
import datetime
from django.utils import timezone



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('__all__')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': 'required',  # Mark this field as required
            }),
            'class_name': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age',
                'min': '1',  # Assuming age must be a positive integer
                'required': 'required',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3,
                'required': 'required',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your contact number',
                'required': 'required',
            }),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        
        # Check if the contact number matches the expected format
        if not re.match(r'^\d{1,3}\d{6,14}$', contact_number):
            raise forms.ValidationError("Phone number must be in the format 'XXXXXXXXXXXX', where the first XX is the country code. You can add a maximum of 15 digits total."
            )
        
        return contact_number

class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name']
        widgets = {
            'class_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Class Name',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Any additional customization can be done here

    def clean_class_name(self):
        class_name = self.cleaned_data.get('class_name')
        if not re.match(r'^\d+[A-Z]$', class_name):
            self.add_error('class_name', "Class name must be in the format '1B', '10C', etc.")
        return class_name




class FeesRecordForm(forms.ModelForm):
    class Meta:
        model = FeesRecord
        fields = ['student', 'amount', 'due_date', 'paid_status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'paid_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        paid_status = self.cleaned_data.get('paid_status')
        if amount <= 0:
            raise forms.ValidationError("The amount must be greater than zero.")
        return amount

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        
        # Ensure the due date is not None
        if due_date is None:
            raise forms.ValidationError("The due date is required.")

        # Check if the due date is in the past
        if due_date < datetime.date.today():
            raise forms.ValidationError("The due date cannot be in the past.")
        
        return due_date
    
    def save(self, commit=True):
        # Call the parent save method to get the FeesRecord instance
        fees_record = super().save(commit=False)
        
        # Set the payment_date if the payment_status is True
        if self.cleaned_data['paid_status']:
            fees_record.payment_date = timezone.now()  # Set the current date and time
        else:
            fees_record.payment_date = None  # Ensure payment_date is None if not paid
        
        if commit:
            fees_record.save()  # Save the instance to the database
            
        return fees_record  # Return the FeesRecord instance

