from django.contrib import admin
from .models import DoctorReport, NurseReport


# Register your models here.
@admin.register(DoctorReport)
class DoctorReport(admin.ModelAdmin):
    list_display = ['title', 'patient', 'get_nurses', 'added_by']

    def get_nurses(self, obj):
        return "\n".join([nurse.user.username for nurse in obj.nurse.all()])

    def patient(self, obj):
        return obj.patient.name

    def get_model_perms(self, request):
        if not request.user.is_admin:
            return {}
        return super(DoctorReport, self).get_model_perms(request)


# Register your models here.
@admin.register(NurseReport)
class NurseReport(admin.ModelAdmin):
    list_display = ['title', 'patient', 'get_doctors', 'added_by']

    def get_doctors(self, obj):
        return "\n".join([doctor.user.username for doctor in obj.doctor.all()])

    def patient(self, obj):
        return obj.patient.name

    def get_model_perms(self, request):
        if not request.user.is_admin:
            return {}
        return super(NurseReport, self).get_model_perms(request)
