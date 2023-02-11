from django.db import models
from users.models import Patient, Nurse, User
import uuid


class Medicines(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Medicines'
        verbose_name_plural = 'Medicines'
        ordering = ['-updated']

    def __str__(self) -> str:
        return self.name


class Medicine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey(
        Medicines, related_name='medicine_name', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    dosage = models.CharField(max_length=100)
    doctor = models.ForeignKey(
        User, related_name='doctor_medicine', on_delete=models.SET_NULL, null=True)
    nurse = models.ManyToManyField(Nurse, related_name='nurse_medicine')
    patient = models.ForeignKey(
        Patient, related_name='patient_medicine', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicine'
        ordering = ['-updated']

    def __str__(self) -> str:
        return self.name.name
