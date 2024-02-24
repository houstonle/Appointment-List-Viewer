from rest_framework import generics, filters
from .models import Patient, NPI, Clinician, Appointment
from .serializers import PatientSerializer, NPISerializer, ClinicianSerializer, AppointmentSerializer


class PatientCreateView(generics.CreateAPIView):
    """
    Creates the patient
    """
    serializer_class = PatientSerializer

class PatientListView(generics.ListAPIView):
    """
    Lists all the patients
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, and deletes a patient
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class NPICreateView(generics.CreateAPIView):
    """
    Creates a new NPI
    """
    serializer_class = NPISerializer

class ClinicianCreateView(generics.CreateAPIView):
    """
    Creates a new Clinician
    """
    serializer_class = ClinicianSerializer

class ClinicianListView(generics.ListAPIView):
    """
    Lists all Clinicians
    """
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer

class ClinicianDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, and deletes a Clinician
    """
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer

class AppointmentCreateView(generics.CreateAPIView):
    """
    Creates a new Appointment
    """
    serializer_class = AppointmentSerializer

class AppointmentListView(generics.ListAPIView):
    """
    Lists all Appointments with optional filtering by date range
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['appointment_date']  # Allow ordering by appointment_date

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            # Filter appointments based on the specified date range
            return Appointment.objects.filter(appointment_date__range=[start_date, end_date])
        else:
            # Return all appointments if no filtering parameters are provided
            return Appointment.objects.all()

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, and deletes an Appointment
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer