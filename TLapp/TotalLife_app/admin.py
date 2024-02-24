from django.contrib import admin
from .models import Patient, NPI, Clinician, Appointment

# Registered models below

admin.site.register(Patient)
admin.site.register(NPI)   
admin.site.register(Clinician)
admin.site.register(Appointment)