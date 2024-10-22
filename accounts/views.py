from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.views.generic import TemplateView,FormView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import LoginForm,CreateUserForm
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login




class LoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    def get(self, request, *args, **kwargs):
            """
            Check if the user is already authenticated
            """
            if request.user.is_authenticated:
                return redirect(self.get_success_url())
            return super().get(request, *args, **kwargs)
        

    def get_success_url(self):
        """
        Redirect users based on their role after successful login.
        """
        user = self.request.user
        #redirect the user based on there roles
        if user.role == 'Admin':
            return reverse_lazy('admin_dashboard') 
        elif user.role == 'Office Staff':
            return reverse_lazy('students')  
        elif user.role == 'Librarian':
            return reverse_lazy('library')
        else:
            return reverse_lazy('login')



class UserCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['Admin']
    model = User
    form_class = CreateUserForm
    template_name = 'accounts/create-user.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()  # Save the user

        # Redirect based on the user's role
        if user.role == 'Admin':
            return redirect('admin_dashboard')
        elif user.role == 'Office Staff':
            return redirect('manage_staff')
        elif user.role == 'Librarian':
            return redirect('manage_librarian')

        return redirect(self.success_url)





class LogoutView(RoleRequiredMixin,LogoutView):
     allowed_roles = ['Admin','Librarian','Office Staff']
     next_page = reverse_lazy('login')


class UserDeleteView(RoleRequiredMixin,DeleteView):
    allowed_roles = ['Admin']

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        if user.role == 'Admin':
            return redirect('admin_dashboard')
        elif user.role == 'Office Staff':
            return redirect('manage_staff')
        elif user.role == 'Librarian':
            return redirect('manage_librarian')
        else:
            return redirect('login')


class UserEditView(RoleRequiredMixin, UpdateView):
    allowed_roles = ['Admin']
    model = User
    template_name = 'accounts/edit-user.html'
    fields = ['username', 'email', 'role']
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        password = self.request.POST.get('password')
        if password:
            user.password = make_password(password)
            form.instance.password = user.password
        user = form.save()
        # Redirect based on the user's role
        if user.role == 'Admin':
            return redirect('admin_dashboard')
        elif user.role == 'Office Staff':
            return redirect('manage_staff')
        elif user.role == 'Librarian':
            return redirect('manage_librarian')
        return redirect(self.success_url)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['email'].widget.attrs.update({'class': 'form-control'})
        form.fields['role'].widget.attrs.update({'class': 'form-select'})
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return super().get_context_data(**kwargs)



    

