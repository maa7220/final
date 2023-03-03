from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .email_Send import send_via_email, send_otp_via_email
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminRole, IsNurse, IsDoctor, IsSuperUser
from .serializer import (SignUpAdminSerializer, SignUpUserSerializer, AddNurseSerializer, UpdateUserSerializer,
                         UserSerializer, SimpleUserSerializer, NurseSerializer, DoctorSerializer, UsersName,
                         AddPatient, PatientSerializer, PatientDoctorsSerializer, PatientNurseSerializer,
                         ResetPasswordSerializer, VerifyOtpSerializer, PasswordSerializer)
from .models import (Admin, Doctor, Nurse, User, Patient)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model
User = get_user_model()


# ---------- SignUp Admin View
class SignUpAdminView(generics.GenericAPIView):
    serializer_class = SignUpAdminSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user).key
            response = {
                "message": "User Created Successfully , wait for accept",
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


# ---- GetPendingAdminUser-------
class GetPendingAdminUser(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = SimpleUserSerializer
    queryset = User.objects.filter(is_active=False)


# ---- Get Pending Details AdminUser -------
class DetailsAdminUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimpleUserSerializer
    queryset = User.objects.all()


# ---- Get Pending Details AdminUser -------
class AccepterAdminUser(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        if not email:
            return Response('Email is required', status=status.HTTP_400_BAD_REQUEST)
        send_via_email(email)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return Response({'Accept'}, status=status.HTTP_200_OK)


# ---- GetActiveAdminUser -------
class GetActiveAdminUser(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = SimpleUserSerializer
    queryset = User.objects.filter(is_active=True, role='admin')


# ---------- SignUp View
class SignUpUserView(generics.GenericAPIView):
    permission_classes = [IsAdminUser, IsAdminRole]
    serializer_class = SignUpUserSerializer

    def post(self, request: Request):
        data = request.data
        user_added = request.user

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save(added_by=user_added)
            response = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully",
                "status": 201
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)


# ---------- Login View
class Login(ObtainAuthToken):

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)
        email = User.objects.filter(email=data.get('username')).exists()

        if email:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            response = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                'token': token.key,
                "massage": "Login Success",
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Email or Password is invalid"}, status=status.HTTP_400_BAD_REQUEST)


# ----- Logout
class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


# -------- Get Login User (Profile)
class LoginUser(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user_id = request.user.id
        queryset = User.objects.get(id=user_id)
        user_serializer = UserSerializer(queryset)
        if user_serializer:
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": user_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----- Add or Remove Nurse from Doctor
class AddDeleteNurseUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole, IsAdminUser]
    serializer_class = AddNurseSerializer

    def post(self, request: Request):
        data = request.data
        doctor = data.get('doctor')
        nurses_ids = data.get('nurse')

        doctor_instance = Doctor.objects.get(user=doctor)
        for nurse_id in nurses_ids:
            nurse_instance = Nurse.objects.get(user_id=nurse_id)
            doctor_instance.nurse.add(nurse_instance)
            self.serializer_class(data=data)
            doctor_instance.save()
        return Response({"message": "Nurse Added successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        data = request.data
        # Get Doctor
        doctor_instance = Doctor.objects.get(user=data['doctor'])
        # Get Nurse For Delete
        nurse_instance = Nurse.objects.get(user=data['nurse'])
        doctor_instance.nurse.remove(nurse_instance)
        return Response({"message": "Nurse deleted"}, status=status.HTTP_204_NO_CONTENT)


# ----- Return Nurses for doctor
class NurseDoctor(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, pk=None):
        try:
            user = request.user
            if pk:
                queryset = Nurse.objects.prefetch_related(
                    'doctor_nurse').get(user_id=pk)
                serializer = NurseSerializer(queryset)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                doctor = Doctor.objects.get(user_id=user.id)
                queryset = doctor.nurse.prefetch_related('doctor_nurse')
                nurses = self.filter_queryset(queryset)
                serializer = NurseSerializer(nurses, many=True)
                return Response({"result": nurses.count(), "nurses": serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# ----- Return Doctors for Nurse
class DoctorNurse(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request, pk=None):
        try:
            user = request.user
            list_doctors = []

            if pk:
                queryset = Doctor.objects.get(user_id=pk)
                serializer = DoctorSerializer(queryset)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                nurse = Nurse.objects.get(user_id=user.id)
                doctors = Doctor.objects.filter(nurse=nurse)

                for doctor in doctors:
                    list_doctors.append(doctor)

                serializer = DoctorSerializer(list_doctors, many=True)

                return Response({"result": len(list_doctors), "doctors": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# -------- Get Doctors (Admin)
class AllDoctors(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'username', 'gender', 'specialization']
    serializer_class = UserSerializer

    def get_queryset(self, pk=None):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.filter(added_by=user).filter(role='doctor')
        else:
            return Response({'message': 'Not Have Access'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------- Get Nurses (Admin)
class AllNurses(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'username', 'gender', 'specialization']
    serializer_class = UserSerializer

    def get_queryset(self,  pk=None):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.filter(added_by=user).filter(role='nurse')
        else:
            return Response({'message': 'Not Have Access'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------- Get Only Users (Updated Delete)
class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = UpdateUserSerializer

    def get(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,  pk=None):
        try:
            user = User.objects.get(id=pk)
            data = request.data
            serializer = self.serializer_class(instance=user, data=data)

            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            response = {
                "message": "User Updated successfully",
                "data": UserSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            user.delete()
            return Response({"message": "User Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# ----- Add Patients -----------
class SignupPatients(generics.GenericAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = AddPatient

    def post(self, request: Request):
        data = request.data
        user_added = request.user
        admin = Admin.objects.get(user_id=user_added.id)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(added_by=admin)
            response = {
                "patient": PatientSerializer(user, context=self.get_serializer_context()).data,
                "message": "Patient Created Successfully",
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response({serializer.errors})


# ----- Patients for admin ---------
class Patients(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'disease_type', 'room_number']
    serializer_class = PatientSerializer

    def get_queryset(self):
        admin = Admin.objects.get(user_id=self.request.user)
        return admin.added_admin.all()


# ----- Patient Details ---------
class PatientDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddPatient
    permission_classes = [IsAdminRole, IsAuthenticated]

    def get(self, request, pk=None):
        try:
            queryset = Patient.objects.get(id=pk)
            data = PatientSerializer(queryset).data
            return Response(data=data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Patient Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            patient = Patient.objects.get(id=pk)
            data = request.data
            serializer = self.serializer_class(instance=patient, data=data)

            serializer.is_valid(raise_exception=True)
            result = serializer.save()
            response = {
                "message": "Patient Updated successfully",
                "patient": PatientSerializer(result).data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Patient Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            queryset = Patient.objects.get(id=pk)
            queryset.delete()
            return Response(data={"message": 'Patient Deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Patient Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# ----- Delete Doctor or Nurse from Patient
class PatientDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]
    serializer_class = AddPatient

    def delete(self, request, pk=None):
        data = request.data

        # Get patient
        patient_instance = Patient.objects.get(id=data['patient'])

        # Get User For Delete
        user = data['user']
        user_instance = User.objects.get(id=user)

        if user_instance.role == 'doctor':
            doctor = Doctor.objects.get(user=user_instance)
            patient_instance.doctor.remove(doctor)
            return Response({"message": "Doctor deleted"}, status=status.HTTP_204_NO_CONTENT)

        else:
            nurse = Nurse.objects.get(user=user_instance)
            patient_instance.nurse.remove(nurse)
            return Response({"message": "Nurse deleted"}, status=status.HTTP_204_NO_CONTENT)


# (Admin) Return Patient For one (nurse , or doctor)
class GetUsersPatient(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]

    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if user.role == 'doctor':
            doctor = Doctor.objects.get(user=user)
            patients = Patient.objects.filter(doctor=doctor)
            serializer = PatientDoctorsSerializer(
                patients, many=True, context=self.get_serializer_context())
            return Response({"result": patients.count(), "patients_data": serializer.data}, status=status.HTTP_200_OK)

        else:
            nurse = Nurse.objects.get(user=user)
            patients = Patient.objects.filter(nurse=nurse)
            serializer = PatientNurseSerializer(
                patients, many=True, context=self.get_serializer_context())
            return Response({"result": patients.count(), "patients_data": serializer.data}, status=status.HTTP_200_OK)


# ----- Return Patient for doctor and nurse
class PatientUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            user = request.user
            if pk:
                queryset = Patient.objects.prefetch_related(
                    'doctor').prefetch_related('nurse').get(id=pk)

                if user.role == 'doctor':
                    serializer = PatientDoctorsSerializer(queryset)

                elif user.role == 'nurse':
                    serializer = PatientNurseSerializer(queryset)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                # --------------------------------
                if user.role == 'doctor':
                    doctor = Doctor.objects.get(user_id=user.id)
                    patients = doctor.doctor.all()
                    serializer = PatientDoctorsSerializer(patients, many=True,)

                # --------------------------------
                elif user.role == 'nurse':
                    nurse = Nurse.objects.get(user_id=user.id)
                    patients = nurse.nurse.all()
                    serializer = PatientNurseSerializer(patients, many=True)

                return Response({"result": patients.count(), "patients_data": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Patient Not Found"}, status=status.HTTP_400_BAD_REQUEST)


class GetRelatedUser(generics.ListCreateAPIView):
    permission_classes = [IsAdminRole, IsAuthenticated]

    def get(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            list_doctors = []
            if user.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                nurses = doctor.nurse.all()
                serializer = NurseSerializer(nurses, many=True)
                return Response({"result": nurses.count(), "nurses": serializer.data}, status=status.HTTP_200_OK)

            elif user.role == 'nurse':
                nurse = Nurse.objects.get(user=user)
                doctors = nurse.doctor_nurse.all()
                for doctor in doctors:
                    list_doctors.append(doctor)
                serializer = DoctorSerializer(list_doctors, many=True)
                return Response({"result": len(list_doctors), "doctors": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorsName(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        doctors = User.objects.filter(role='doctor')
        serializer = UsersName(doctors, many=True).data
        return Response(serializer)


class NursesName(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        nurses = User.objects.filter(role='nurse')
        serializer = UsersName(nurses, many=True).data
        return Response(serializer)


# ============================================================================
# Reset Password
# ============================================================================
class PasswordResetView(APIView):

    def post(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"message": 'Invalid Email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                send_otp_via_email(email)
                return Response({"message": 'code sent'}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):

    def post(self, request):
        data = request.data
        serializer = VerifyOtpSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response({"message": 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp != otp:
                return Response({"message": 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            if user[0].otp == otp:
                return Response({"message": "code done", "code": otp}, status=status.HTTP_200_OK)
        else:
            return Response({"message": 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    def post(self, request):
        data = request.data

        serializer = PasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.data['password']
            email = serializer.data['email']
            user = User.objects.get(email=email)

            user.password = make_password(password)
            user.save()
            print(user.password)

            return Response({"message": ""}, status=status.HTTP_201_CREATED)
