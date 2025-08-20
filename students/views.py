from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,DeleteView,CreateView,UpdateView,ListView
from accounts.mixins import RoleRequiredMixin
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from django.http import JsonResponse
from library.models import LibraryRecord
 


# Create your views here.
class StudentsView(RoleRequiredMixin, TemplateView):
    allowed_roles = ['Office Staff', 'Admin']
    template_name = 'students/students.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        context['total_students'] = Student.objects.all().count()
        context['total_fee_due'] = FeesRecord.objects.filter(paid_status=False).count()
        context['total_class'] = Class.objects.all().count()
        context['total_librarians'] = 10

        return context


"""
Views for Students Model
"""

class StudentManageView(RoleRequiredMixin,ListView):
    template_name='students/std/students_manage.html'
    allowed_roles = ['Office Staff', 'Admin']
    model = Student
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classlist'] = Class.objects.all()
        return context

class CreateStudentView(RoleRequiredMixin,CreateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Student
    form_class = StudentForm
    template_name = 'students/std/create-student.html'
    success_url = reverse_lazy('student_manage')

class EditStudentView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Student
    form_class = StudentForm
    template_name = 'students/std/edit-student.html'
    success_url = reverse_lazy('student_manage')


class DeleteStudentView(RoleRequiredMixin,DeleteView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Student
    def post(self, request, pk):
        std = get_object_or_404(Student, pk=pk)
        std.delete()
        return redirect('student_manage')

class StudentSearchView(RoleRequiredMixin, ListView):
    allowed_roles = ['Office Staff', 'Admin']

    def get(self, request):
        query = request.GET.get('q', '')
        class_name = request.GET.get('class', '')
        gender = request.GET.get('gender', '')
        age = request.GET.get('age', '') 
        address = request.GET.get('address','')

        students = Student.objects.all()
        # Apply search by name
        if query:
            students = students.filter(full_name__icontains=query)

        # Apply class filter
        if class_name:
            students = students.filter(class_name__class_name=class_name.upper())
        if address:
            students = students.filter(address__icontains=address)

        # Apply gender filter
        if gender:
            students = students.filter(gender=gender)

        # Apply age filter
        if age.isdigit():
            students = students.filter(age=int(age))
        
        students_list = list(students.values(
            'id', 'full_name', 'class_name__class_name', 'age', 'gender', 'address', 'contact_number'
        ))
        return JsonResponse({'users': students_list})


    
"""
Views for Fee Model
"""
class  FeeView(RoleRequiredMixin, ListView):
    allowed_roles = ['Office Staff', 'Admin']
    model = FeesRecord
    template_name = 'students/fee/fee_manage.html'
    context_object_name = 'fees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classlist'] = Class.objects.all()
        return context



class  CreateFeeView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = FeesRecord
    form_class = FeesRecordForm
    template_name = 'students/fee/create_fee.html'
    success_url = reverse_lazy('fee')
    

class  EditFeeView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = FeesRecord
    form_class = FeesRecordForm
    template_name = 'students/fee/edit_fee.html'
    success_url = reverse_lazy('fee')


class DeleteFeeView(RoleRequiredMixin,DeleteView):
    allowed_roles = ['Office Staff', 'Admin']
    model = FeesRecord
    def post(self, request, pk):
        fee = get_object_or_404(FeesRecord, pk=pk)
        fee.delete()
        return redirect('fee')
    

class FeeSearchView(RoleRequiredMixin,ListView):
    allowed_roles = ['Office Staff', 'Admin']
    
    def test_func(self):
        return self.request.user.role in self.allowed_roles

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        class_name = self.request.GET.get('class', '')
        gender = self.request.GET.get('gender', '')
        age = self.request.GET.get('age', '')
        address = self.request.GET.get('address', '')
        paid_status = self.request.GET.get('paid_status', '')
        min_fee = self.request.GET.get('min_fee', '')
        max_fee = self.request.GET.get('max_fee', '')
        due_date = self.request.GET.get('due_date', '')


        fees = FeesRecord.objects.prefetch_related('student')

        # Apply search by name
        if query:
            fees = fees.filter(student__full_name__icontains=query)

        # Apply filters based on input
        if class_name:
            fees = fees.filter(student__class_name__class_name=class_name.upper())
        if address:
            fees = fees.filter(student__address__icontains=address)
        if gender:
            fees = fees.filter(student__gender=gender)
        if age.isdigit():
            fees = fees.filter(student__age=int(age))
        if paid_status in ['true', 'false']:
            fees = fees.filter(paid_status=paid_status.lower() == 'true')
        if min_fee.isdigit():
            fees = fees.filter(amount__gte=int(min_fee))
        if max_fee.isdigit():
            fees = fees.filter(amount__lte=int(max_fee))
        if due_date:
            fees = fees.filter(due_date=due_date)

        return fees

    def get(self, request, *args, **kwargs):
        # Get the filtered queryset
        fees = self.get_queryset()


        students_list = list(fees.values(
            'id', 
            'student__full_name', 
            'student__class_name__class_name', 
            'student__age', 
            'student__gender', 
            'student__address', 
            'student__contact_number',
            'amount',
            'due_date',
            'paid_status',
            'payment_date',
        ))
        
        return JsonResponse({'users': students_list})


"""
Views for Class Model
"""
class ClassView(RoleRequiredMixin, TemplateView):
    allowed_roles = ['Office Staff', 'Admin']
    template_name = 'students/class/class.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all().order_by('class_name')
        return context
    
class ClassCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Class
    form_class = ClassCreateForm
    template_name='students/class/create-class.html'
    success_url = reverse_lazy('class_manage')

    def form_valid(self, form):
        class_name = form.cleaned_data['class_name'].upper()
        if Class.objects.filter(class_name=class_name).exists():
            form.add_error('class_name', 'Class with this Class name already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)

class ClassEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Class
    form_class = ClassCreateForm
    template_name='students/class/edit-class.html'
    success_url = reverse_lazy('class_manage')

    def form_valid(self, form):
        class_name = form.cleaned_data['class_name'].upper()
        if Class.objects.filter(class_name=class_name).exists():
            form.add_error('class_name', 'Class with this Class name already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)

class ClassDeleteView(RoleRequiredMixin, DeleteView):
    allowed_roles = ['Office Staff', 'Admin']
    model = Class
    def post(self, request, pk):
        user = get_object_or_404(Class, pk=pk)
        user.delete()
        return redirect('class_manage')
    
    
