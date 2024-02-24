# app_folder/urls.py
from django.urls import path
from .views import PatientCreateView, PatientListView, PatientDetailView, ClinicianCreateView, ClinicianListView, ClinicianDetailView, NPICreateView, AppointmentCreateView, AppointmentListView, AppointmentDetailView

urlpatterns = [
    path('patients/create/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('npi/create/', NPICreateView.as_view(), name='npi_create'),
    path('clinicians/create/', ClinicianCreateView.as_view(), name='clinician_create'),
    path('clinicians/', ClinicianListView.as_view(), name='clinician_list'),
    path('clinicians/<int:pk>/', ClinicianDetailView.as_view(), name='clinician_detail'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
]
