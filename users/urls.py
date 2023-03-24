from django.urls import path
from .views import (SignUpAdminView, GetActiveAdminUser, SignUpUserView, Login,
                    LogoutView, LoginUser, AddDeleteNurseUser, NurseDoctor, DoctorNurse, AllDoctors, AllNurses,
                    GetPendingAdminUser, DetailsAdminUser, AccepterAdminUser, UserDetails, SignupPatients,
                    Patients, PatientDetailsAPI, PatientDeleteUser, GetUsersPatient, GetRelatedUser,
                    PasswordResetView, VerifyOTP, PasswordView, DoctorsName, NursesName, PatientUser, UpdateProfileAdmin
                    )


urlpatterns = [
    # ----------AUTH -------------
    path("signup_admin", SignUpAdminView.as_view(), name="signup_admin"),
    path("signup_user", SignUpUserView.as_view(), name="signup_user"),
    path("login", Login.as_view(), name="login"),

    path("update_profile",
         UpdateProfileAdmin.as_view(), name="update_profile"),

    # ============================================================================
    # Reset Password
    # ============================================================================
    path("send_code", PasswordResetView.as_view(), name="send_code"),
    path("verify_otp", VerifyOTP.as_view(), name="verify_oTP"),
    path("password_confirm", PasswordView.as_view(), name="password_confirm"),

    # User Profile
    path("user/profile", LoginUser.as_view(), name="profile"),

    path("doctors_name", DoctorsName.as_view(), name="doctors_name"),
    path("nurses_name", NursesName.as_view(), name="nurses_name"),


    # ----------Get Admin -------------
    path("active_admin", GetActiveAdminUser.as_view(), name="active_admin"),
    path("pending_admin", GetPendingAdminUser.as_view(), name="pending_admin"),
    path("pending_admin/<str:pk>", DetailsAdminUser.as_view(),
         name="pending_admin_details"),

    path("accept_admin", AccepterAdminUser.as_view(),
         name="accept_admin"),
    # ---------- get users -------------
    path("get_related_user/<str:pk>",
         GetRelatedUser.as_view(), name="get_related_user"),

    # Return All Doctors
    path("doctors/", AllDoctors.as_view(), name="doctors"),

    # Return All Nurses
    path("nurses/", AllNurses.as_view(), name="nurses"),

    # User Details
    path("user/<str:pk>", UserDetails.as_view(), name="user_detail"),

    # Add Nurse for doctor
    path("add_nurses", AddDeleteNurseUser.as_view(), name="nurse_doctor"),
    path("delete_nurses_doctor", AddDeleteNurseUser.as_view(), name="nurse_doctor"),

    # Return Nurse For doctor
    path("nurse/", NurseDoctor.as_view(), name="nurses_doctor"),
    path("nurse/<str:pk>", NurseDoctor.as_view(), name="nurses_doctor"),

    # Return Doctor For Nurse
    path("doctor/", DoctorNurse.as_view(), name="doctors_nurse"),
    path("doctor/<str:pk>", DoctorNurse.as_view(), name="doctor_nurse"),


    # ----------------PatientAPI---------------
    path("add-patient", SignupPatients.as_view(), name="add_patient"),
    path("patients/", Patients.as_view(), name="patients"),
    path("patients/<str:pk>", PatientDetailsAPI.as_view(), name="patient-details"),
    path("delete_patients_user", PatientDeleteUser.as_view(),
         name="delete_patients_user"),
    # ====== (Admin) Return Patient For one (nurse , or doctor)
    path("get_patients_user/<str:pk>",
         GetUsersPatient.as_view(), name="patients_user"),

    # =================== Return Patient For one doctor or nurse (Login) =========
    path("patient_user/", PatientUser.as_view(), name="patients_user"),
    path("patient_user/<str:pk>",
         PatientUser.as_view(), name="patients_user"),
]
