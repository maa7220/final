from django.contrib import admin
from .models import (User, Admin, Doctor, Nurse, Patient)

# =========== User ==============


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'username', 'role']
    list_per_page = 20
    search_fields = ['username', 'role']

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        users_admin = qs.filter(role='admin')
        users = qs.filter(added_by=request.user)

        if request.user.role == 'admin':
            return users

        if request.user.is_superuser and request.user.role != 'admin':
            return users_admin


# =========== Admin ==============
@admin.register(Admin)
class AdminModel(admin.ModelAdmin):
    list_display = ['username', 'name', 'email']
    list_per_page = 10

    def username(self, obj):
        return (obj.user.username)

    def email(self, obj):
        return (obj.user.email)

    def name(self, obj):
        return (obj.user.name)

    def get_model_perms(self, request):
        if request.user.role == 'admin':
            return {}
        return super(AdminModel, self).get_model_perms(request)


# =========== Doctor ==============
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email']
    list_per_page = 10

    def username(self, obj):
        return (obj.user.username)

    def email(self, obj):
        return (obj.user.email)

    def name(self, obj):
        return (obj.user.name)

    def get_model_perms(self, request):
        if not request.user.is_admin:
            return {}
        return super(DoctorAdmin, self).get_model_perms(request)


# =========== Nurse ==============
@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email']
    list_per_page = 10

    def username(self, obj):
        return (obj.user.username)

    def email(self, obj):
        return (obj.user.email)

    def name(self, obj):
        return (obj.user.name)

    def get_model_perms(self, request):
        if not request.user.is_admin:
            return {}
        return super(NurseAdmin, self).get_model_perms(request)


# =========== Patient ==============
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'disease_type', 'gender',
                    'age', 'room_number', 'doctors', 'nurses']
    search_fields = ['name', 'room_number', 'age', 'gender']
    list_per_page = 12

    def doctors(self, obj):
        for doctor in obj.doctor.all():
            return (doctor)

    def nurses(self, obj):
        for nurse in obj.nurse.all():
            return (nurse)

    def get_model_perms(self, request):
        if not request.user.is_admin:
            return {}
        return super(PatientAdmin, self).get_model_perms(request)
