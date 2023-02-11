from rest_framework import serializers
from .models import Nurse, DoctorReport, NurseReport, Doctor


class DoctorReportSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.all(), many=True)

    class Meta:
        model = DoctorReport
        fields = ['title', 'nurse', 'patient']


class ResultDoctorReportSerializer(serializers.ModelSerializer):
    nurse = serializers.SerializerMethodField(source='get_nurse')
    patient = serializers.StringRelatedField()

    class Meta:
        model = DoctorReport
        fields = ['id', 'title', 'nurse', 'patient', 'created', 'updated']

    # ========= Get Nurse Information
    @staticmethod
    def get_nurse(obj):
        nurse_list = []
        nurse = obj.nurse.all()
        for i in nurse:
            data = i.user
            nurse_list.append({"name": data.name})
        return nurse_list


class ResultDoctorReportAddedNurseSerializer(serializers.ModelSerializer):
    nurse = serializers.StringRelatedField(source='added_by')
    patient = serializers.StringRelatedField()

    class Meta:
        model = NurseReport
        fields = ['id', 'title', 'nurse', 'patient', 'created', 'updated']


# =================== Nurse ===========================================
class NurseReportSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Doctor.objects.all(), many=True)

    class Meta:
        model = NurseReport
        fields = ['title', 'doctor', 'patient']


class ResultNurseReportSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField(source='get_doctor')
    patient = serializers.StringRelatedField()

    class Meta:
        model = NurseReport
        fields = ['id', 'title', 'doctor', 'patient', 'created', 'updated']

        # ========= Get Doctor Information

    @staticmethod
    def get_doctor(obj):
        doctor_list = []
        doctor = obj.doctor.all()
        for i in list(doctor):
            data = i.user
            doctor_list.append({"name": data.name})

        return doctor_list


class ResultNurseReportAddedDoctorSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(source='added_by')
    patient = serializers.StringRelatedField()

    class Meta:
        model = DoctorReport
        fields = ['id', 'title', 'doctor', 'patient', 'created', 'updated']


# =================== Patient ===========================================
class ReportDoctorPatientSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Nurse.objects.all(), many=True)

    class Meta:
        model = DoctorReport
        fields = ['title', 'created', 'nurse', 'patient']


class ReportNursePatientSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        slug_field="user_id", queryset=Doctor.objects.all(), many=True)

    class Meta:
        model = NurseReport
        fields = ['title', 'created', 'doctor', "patient"]


class DoctorReportAllNursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReport
        fields = ['title', 'patient']


class NurseReportAllDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseReport
        fields = ['title', 'patient']
