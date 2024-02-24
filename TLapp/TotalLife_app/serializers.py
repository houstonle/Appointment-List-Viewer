from rest_framework import serializers
from .models import Patient, NPI, Clinician, Appointment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class NPISerializer(serializers.ModelSerializer):
    class Meta:
        model = NPI
        fields = '__all__'

class ClinicianSerializer(serializers.ModelSerializer):
    npi = NPISerializer()

    class Meta:
        model = Clinician
        fields = '__all__'

    def create(self, validated_data):
        # Extract the nested NPI data
        npi_data = validated_data.pop('npi', None)

        # Create the NPI instance
        npi_instance = NPI.objects.create(**npi_data)

        # Create the Clinician instance with the NPI instance
        clinician_instance = Clinician.objects.create(npi=npi_instance, **validated_data)

        return clinician_instance

class AppointmentSerializer(serializers.ModelSerializer):
    # First two lines make it so that you can only select patients and clinicians that exists
    #patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    patient_name = serializers.CharField(source='get_patient_name', read_only=True)
    clinician = serializers.PrimaryKeyRelatedField(queryset=Clinician.objects.all())

    class Meta:
        model = Appointment
        fields = '__all__'
