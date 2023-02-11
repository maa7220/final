from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (Admin, User, Doctor, Nurse, Patient)


# --------- User Serializer
class UserSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "phone", "added_by",
                  'nat_id', 'image', 'specialization', "role",  "gender", "age"]


# --------- Simple User Serializer
class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "name", "phone"]


# --------- SignUp Admin Serializer
class SignUpAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "name", "phone", "password"]

    extra_kwargs = {
        'email': {'required': True},
        'username': {'required': True},
        'name': {'required': True},
        'phone': {'required': True},
        'password': {'required': True},
    }

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exists = User.objects.filter(
            username=attrs["username"]).exists()
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        if username_exists:
            raise ValidationError("Username has already been used")
        if phone_exists:
            raise ValidationError("Phone has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data['role'] = 'admin'

        if validated_data['role'] == 'admin':
            validated_data['is_admin'] = True
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
            validated_data['is_active'] = False

        user = super().create(validated_data)
        user.set_password(password)

        if user.is_admin == True:
            user.save()
            Admin.objects.create(user=user)
        user.save()
        return user


# --------- SignUp Serializer
class SignUpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "name", "phone", 'image', 'nat_id',
                  "password", "role", "gender", "age", "specialization"]

    extra_kwargs = {
        'role': {'required': True},
    }

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exists = User.objects.filter(
            username=attrs["username"]).exists()
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()
        nat_exists = User.objects.filter(nat_id=attrs["nat_id"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        if username_exists:
            raise ValidationError("Username has already been used")
        if phone_exists:
            raise ValidationError("Phone has already been used")
        if nat_exists:
            raise ValidationError("ID must be unique")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        if validated_data['role'] == 'doctor':
            validated_data['is_doctor'] = True

        elif validated_data['role'] == 'nurse':
            validated_data['is_nurse'] = True

        user = super().create(validated_data)
        user.set_password(password)

        if user.is_doctor == True:
            Doctor.objects.create(user=user)
            user.save()

        if user.is_nurse == True:
            Nurse.objects.create(user=user)
            user.save()
        user.save()
        return user


# Add Nurse to doctor
class AddNurseSerializer(serializers.ModelSerializer):
    nurse = serializers.SlugRelatedField(
        queryset=Nurse.objects.all(), many=True, slug_field='user_id')

    class Meta:
        model = Doctor
        fields = ["doctor", "nurse"]


# Return Nurses User
class NurseSerializer(serializers.ModelSerializer):
    nurse = SimpleUserSerializer(source='user')

    class Meta:
        model = Nurse
        fields = ["nurse"]


# Return Doctor User
class DoctorSerializer(serializers.ModelSerializer):
    doctor = SimpleUserSerializer(source='user')

    class Meta:
        model = Doctor
        fields = ["doctor"]


# Updated Profile
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "name",
                  "phone", "role", "gender", "age"]

        def validate(self, value):
            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use."})

            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError(
                    {"username": "This username is already in use."})
            return value

        def update(self, instance, validated_data):
            user = self.context['request'].user

            if user.pk != instance.pk:
                raise serializers.ValidationError(
                    {"authorize": "You dont have permission for this user."})

            instance.name = validated_data['name']
            instance.email = validated_data['email']
            instance.username = validated_data['username']
            instance.save()

            return instance


# --------- Add Patient
class AddPatient(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(
        queryset=Doctor.objects.all(), many=True, slug_field='user_id')
    nurse = serializers.SlugRelatedField(
        queryset=Nurse.objects.all(), many=True, slug_field='user_id')

    class Meta:
        model = Patient
        fields = ["name", "image", "doctor", 'nurse', 'address',
                  'disease_type', 'room_number', 'nat_id', 'phone', 'gender', 'age', 'status']

    def validate(self, attrs):
        nat_id_exists = Patient.objects.filter(nat_id=attrs["nat_id"]).exists()
        phone_exists = Patient.objects.filter(phone=attrs["phone"]).exists()
        if phone_exists:
            raise ValidationError("Phone has already been used")
        if nat_id_exists:
            raise ValidationError("ID has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        patient = super().create(validated_data)
        patient.save()
        return patient


# Patient ---------
class PatientSerializer(serializers.ModelSerializer):
    nurse = serializers.SerializerMethodField(source='get_nurse')
    doctor = serializers.SerializerMethodField(source='get_doctor')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image', 'disease_type', 'room_number', 'address',
                  'nat_id', 'phone', 'gender', 'age', 'status', 'doctor', 'nurse']
        depth = 1

    # ========= Get Doctor Information
    @staticmethod
    def get_doctor(obj):
        doctor_list = []
        doctor = obj.doctor.all()
        for i in list(doctor):
            data = i.user
            doctor_list.append({"id": data.id, "username": data.username,
                                "image": data.image.url,  'phone': f'{data.phone}'})

        return doctor_list

    # ========= Get Nurse Information
    @staticmethod
    def get_nurse(obj):
        nurse_list = []
        nurse = obj.nurse.all()
        for i in nurse:
            data = i.user
            print(data.phone)
            nurse_list.append({"id": data.id, "username": data.username,
                               "image": data.image.url, 'phone': f'{data.phone}'})
        return nurse_list


# ----- Return Patient for doctor and nurse
class PatientDoctorsSerializer(serializers.ModelSerializer):
    nurse = serializers.SerializerMethodField(source='get_nurse')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image', 'disease_type', 'room_number', 'address',
                  'phone',  'age', 'status', 'nurse']

    # ========= Get Nurse Information

    @staticmethod
    def get_nurse(obj):
        nurse_list = []
        nurse = obj.nurse.all()
        for i in nurse:
            data = i.user
            nurse_list.append({"id": data.id, "username": data.username,
                               "image": data.image.url, 'phone': f'{data.phone}'})
        return nurse_list


# ----- Return Patient for doctor and nurse
class PatientNurseSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField(source='get_doctor')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'image', 'disease_type', 'room_number',
                  'phone',  'age', 'status', 'doctor']

    # ========= Get Doctor Information
    @staticmethod
    def get_doctor(obj):
        doctor_list = []
        doctor = obj.doctor.all()
        for i in list(doctor):
            data = i.user
            doctor_list.append({"id": data.id, "username": data.username,
                                "image": data.image.url, 'phone': f'{data.phone}'})
        return doctor_list


class UsersName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# ============================================================================
# Reset Password
# ============================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
