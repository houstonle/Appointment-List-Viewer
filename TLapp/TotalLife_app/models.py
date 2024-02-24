from django.db import models
from django.utils import timezone
import requests

class Patient(models.Model):
    '''
    Model for a patient
    first_name: first name of the patient
    last_name: last name of the patient
    age: patient age
    gender: choice of: Male, Female, or Other
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age} {self.gender}'

class NPI(models.Model):
    '''
    Model for a NPI. This is a unique identification number for covered health care proviers in the US
    npi_number: the NPI number
    first_name: first name of the clinician
    last_name: last name of the clinician
    state: state where the clinician operates
    '''
    npi_number = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.npi_number} {self.first_name} {self.last_name} {self.state}'
    
    def save(self, *args, **kwargs):
        # Call the validation method before saving
        if self.validate_with_npi_registry():
            super().save(*args, **kwargs)
        else:
            # Handle validation failure, for example, raise an exception
            raise ValueError("NPI validation failed")
        
    def validate_with_npi_registry(self):
        formatted_num = self.npi_number
        api_url = "https://npiregistry.cms.hhs.gov/api/?number="+formatted_num+"&version=2.1"
        
        # Make the API request
        response = requests.get(api_url)
        data = response.json()

        if data.get('result_count', 0) == 1:
            # Validate state, first name, and last name
            result = data.get('results', [])[0]
            addresses = result.get('addresses', [])
            if addresses and addresses[0].get('state') == self.state:
                basic_info = result.get('basic', {})
                if (
                    basic_info.get('first_name', '').upper() == self.first_name.upper()
                    and basic_info.get('last_name', '').upper() == self.last_name.upper()
                ):
                    return True
            return False
        else:
            return False

class Clinician(models.Model):
    '''
    Model for a Clinician. Clinicians must have an NPI
    first_name: first name of the clinician
    last_name: last name of the clinician
    specialization: specialization of the clinician
    npi: NPI number of the clinician. Note that clinicnas must have an NPI
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    npi = models.OneToOneField(NPI, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.specialization} {self.npi}'
    
    def save(self, *args, **kwargs):
        # Call the validation method before saving
        if self.npi.validate_with_npi_registry():
            super().save(*args, **kwargs)
        else:
            # Handle validation failure, for example, raise an exception
            raise ValueError("NPI validation failed")

class Appointment(models.Model):
    '''
    Model for an appointment
    patient: patient who has the appointment
    clinicina: clinician who is seeing the patient
    appointment_date: date and time of the appointment
    duration_minutes: duration of the appointment in minutes
    reason_for_visit: reason for the appointment
    '''
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(default=timezone.now)
    appointment_status = models.CharField(max_length=10, choices=[('S', 'Scheduled'), ('C', 'Cancelled'), ('D', 'Done')], default='S')
    duration_minutes = models.IntegerField()
    reason_for_visit = models.TextField()

    def __str__(self):
        return f'{self.patient} {self.clinician} {self.appointment_date} {self.appointment_status} {self.duration_minutes} {self.reason_for_visit}'
    
    def get_patient_name(self):
        return f'{self.patient.first_name} {self.patient.last_name}'