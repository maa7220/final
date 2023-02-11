from django.db import models
from users.models import Nurse, Patient, Doctor


class DoctorReport(models.Model):
    nurse = models.ManyToManyField(Nurse, related_name='nurse_reports')

    patient = models.ForeignKey(
        Patient, models.CASCADE, related_name='patient_reports', null=True)

    added_by = models.ForeignKey(
        Doctor, models.CASCADE, related_name='doctor_reports', null=True)

    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor Report'
        verbose_name_plural = 'Doctor Report'
        ordering = ['-created']

    def __str__(self):
        return self.title


class NurseReport(models.Model):
    doctor = models.ManyToManyField(Doctor, related_name='doctors_reports')

    patient = models.ForeignKey(
        Patient, models.CASCADE, related_name='patients_reports', null=True)

    added_by = models.ForeignKey(
        Nurse, models.CASCADE, related_name='nurses_reports', null=True)

    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nurse Report'
        verbose_name_plural = 'Nurse Report'
        ordering = ['-created']

    def __str__(self):
        return self.title
