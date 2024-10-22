from django.urls import path
from . import views

urlpatterns = [
    path('',views.StudentsView.as_view(),name='students'),

    path('manage',views.StudentManageView.as_view(),name='student_manage'),
    path('create',views.CreateStudentView.as_view(),name='create_student'),
    path('<int:pk>/edit',views.EditStudentView.as_view(),name='edit_student'),
    path('<int:pk>/delete',views.DeleteStudentView.as_view(),name='delete_student'),
    path('search_student',views.StudentSearchView.as_view(),name='search_student'),
    


    path('fee',views.FeeView.as_view(),name='fee'),
    path('fee/create',views.CreateFeeView.as_view(),name='create_fee'),
    path('fee/<int:pk>/edit',views.EditFeeView.as_view(),name='edit_fee'),
    path('fee/<int:pk>/delete',views.DeleteFeeView.as_view(),name='delete_fee'),
    path('search_fee',views.FeeSearchView.as_view(),name='search_fee'),

    path('classes',views.ClassView.as_view(),name='class_manage'),
    path('classes/create',views.ClassCreateView.as_view(),name='class_create'),
    path('classes/<int:pk>/edit',views.ClassEditView.as_view(),name='class_edit'),
    path('classes/<int:pk>/delete',views.ClassDeleteView.as_view(),name='class_delete'),

]