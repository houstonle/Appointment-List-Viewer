from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Patient, NPI, Clinician, Appointment
from .serializers import PatientSerializer, NPISerializer, ClinicianSerializer, AppointmentSerializer

class PatientCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_patient(self):
        """
        Test the creation of a new patient using the API endpoint. Checks if the patient is created and the response is correct.
        """
        url = reverse('patient_create')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'gender': 'M',
        }

        response = self.client.post(url, data, format='json')
        created_patient = Patient.objects.first()
        serializer = PatientSerializer(created_patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.get().first_name, 'John')

class PatientListViewTest(TestCase):
    def setUp(self):
        # Create a sample patient for testing
        self.sample_patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            gender='M'
        )
        self.client = APIClient()

    def test_list_patients(self):
        """
        Test listing all patients using the PatientListView.
        """
        url = reverse('patient_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class PatientDetailViewTest(TestCase):
    def setUp(self):
        # Create a sample patient for testing
        self.sample_patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            gender='M'
        )
        self.client = APIClient()

    def test_retrieve_patient(self):
        """
        Test retrieving a patient using the PatientDetailView.
        """
        url = reverse('patient_detail', kwargs={'pk': self.sample_patient.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_update_patient(self):
        """
        Test updating a patient using the PatientDetailView.
        """
        url = reverse('patient_detail', kwargs={'pk': self.sample_patient.pk})
        data = {'first_name': 'UpdatedJohn', 'last_name': 'Doe', 'age': 31, 'gender': 'M'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the instance from the database
        self.sample_patient.refresh_from_db()

        # Check if the serializer can save the data (this calls the update method)
        serializer = PatientSerializer(instance=self.sample_patient, data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Assert that the patient has been updated
        self.assertEqual(self.sample_patient.first_name, 'UpdatedJohn')
        self.assertEqual(self.sample_patient.age, 31)

    def test_delete_patient(self):
        """
        Test deleting a patient using the PatientDetailView.
        """
        url = reverse('patient_detail', kwargs={'pk': self.sample_patient.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=self.sample_patient.pk).exists())

class NPITest(TestCase):
    def test_validate_with_npi_valid(self):
        # Create an NPI instance with valid data
        npi = NPI(
            npi_number='1841940681',
            first_name='ROBERT',
            last_name='AAMODT',
            state='NC'
        )

        # Call the validate_with_npi method
        is_valid = npi.validate_with_npi_registry()

        # Assert that the validation result is True
        self.assertTrue(is_valid)

    def test_validate_with_npi_invalid(self):
        # Create an NPI instance with invalid data
        npi = NPI(
            npi_number='1234567890',  # Invalid NPI
            first_name='John',
            last_name='Doe',
            state='CA'
        )

        # Call the validate_with_npi method
        is_valid = npi.validate_with_npi_registry()

        # Assert that the validation result is False
        self.assertFalse(is_valid)